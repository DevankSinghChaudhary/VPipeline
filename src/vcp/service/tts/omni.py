import time

import soundfile as sf
import torch
from langgraph.types import Send
from omnivoice import OmniVoice

from vcp.state import GlobalState
from vcp.utils import root

MAX_CONCURRENCY = 8  # MAX BATCHED TTS INPUT

BASE = root.find()

AUDIO_PATH = BASE / "renderer/public/audio"

REF = BASE / "src" / "vcp" / "service" / "tts" / "assets" / "ref.mp3"

REF_AUDIO = str(REF)


def fanout_tts(state: GlobalState):
    scripts = state["script"].script
    start = state["tts_index"]

    batch = scripts[start : start + MAX_CONCURRENCY]

    return [
        Send(
            "Omni",
            {
                "script_for_tts": script,
            },
        )
        for script in batch
    ]


def tts_batch_complete(state: GlobalState):
    return {"tts_index": state["tts_index"] + MAX_CONCURRENCY}


model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16
)


def omni(state: fanout_tts):

    start = time.time()

    script = state["script_for_tts"]
    id = script.id
    text = script.script

    print(f"[SERVICE] Omni | Generating {id}...")

    audio = model.generate(
        text=text,
        ref_audio=REF_AUDIO,
        ref_text="The McLaren 720S demonstrates exceptional aerodynamic efficiency with its 4.0-liter twin-turbocharged V8 engine",
    )

    output = AUDIO_PATH / f"{id}.wav"

    sf.write(output, audio[0], 24000)

    print(f"[SERVICE] Omni | Finished {id} | {time.time() - start:.2f}s")

    return {"audio": [str(output)]}
