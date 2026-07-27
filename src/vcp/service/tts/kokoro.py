import os
import time
import shutil
from pathlib import Path

import soundfile as sf
from dotenv import load_dotenv
from kokoro import KPipeline
from langgraph.types import Send

from vcp.state import GlobalState


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

def find_project_root() -> Path:
    current = Path(__file__).resolve()

    for directory in (current, *current.parents):
        if (directory / ".env").exists():
            return directory

    raise FileNotFoundError(
        "Couldn't find .env in project root"
    )


PROJECT_ROOT = find_project_root()

load_dotenv(PROJECT_ROOT / ".env")


AUDIO_PATH = Path(
    os.getenv(
        "AUDIO_PATH",
        "src/vcp/output"
    )
)

if AUDIO_PATH.exists():
    shutil.rmtree(AUDIO_PATH)

if not AUDIO_PATH.is_absolute():
    AUDIO_PATH = PROJECT_ROOT / AUDIO_PATH

AUDIO_PATH.mkdir(
    parents=True,
    exist_ok=True
)

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

VOICE = os.getenv("VOICE")

SPEED = float(
    os.getenv(
        "TTS_SPEED",
        "1.122"
    )
)

SAMPLE_RATE = 24000


# --------------------------------------------------
# MODEL
# --------------------------------------------------

pipeline = KPipeline(
    lang_code="a"
)


# --------------------------------------------------
# FANOUT
# --------------------------------------------------

def fanout_tts(state: GlobalState):
    return [
        Send(
            "Kokoro", {
                "script_for_kokoro": script
            }
        )
        for script in state["script"].script
    ]


# --------------------------------------------------
# TTS SERVICE
# --------------------------------------------------

def kokoro_service(script: GlobalState):
    start = time.time()

    script_id = script["script_for_kokoro"].id
    text = script["script_for_kokoro"].script

    print(
        f"[SERVICE] Kokoro | "
        f"Converting script {script_id}..."
    )

    engine = pipeline(
        text,
        voice=VOICE,
        speed=SPEED
    )

    output_path = (
        AUDIO_PATH / f"{script_id}.wav"
    )

    for _, _, audio in engine:

        sf.write(
            output_path,
            audio,
            SAMPLE_RATE
        )

        break

    print(
        f"[SERVICE] Kokoro | "
        f"Finished script {script_id} | "
        f"{time.time() - start:.2f}s"
    )

    return {
        "audio": [str(output_path)]
    }
