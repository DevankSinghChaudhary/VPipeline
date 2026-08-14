from vcp.utils import root
from vcp.state import GlobalState

from omnivoice import OmniVoice
import soundfile as sf
import torch
import time

from langgraph.types import Send


MAX_CONCURRENCY = 8 #MAX BATCHED TTS INPUT

BASE = root.find()

AUDIO_PATH = BASE / "src" / "vcp" / "output"

REF = BASE / "src" / "vcp" / "service" / "tts" / "assets" / "narrator.mp3"

REF_AUDIO = str(REF)


def fanout_tts(state: GlobalState):
    scripts = state["script"].script
    start = state["tts_index"]

    batch = scripts[start:start + MAX_CONCURRENCY]

    if not batch:
        return "Merger"

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
    return {
        "tts_index": state["tts_index"] + MAX_CONCURRENCY
    }


model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map="cuda:0",
    dtype=torch.float16
)

def omni(state: fanout_tts):
    
    start = time.time()

    script = state["script_for_tts"]
    id = script.id
    text = script.script

    print(
        f"[SERVICE] Omni | "
        f"Generating {id}..."
    )

    audio = model.generate(
        text=text,
        ref_audio=REF_AUDIO,
        ref_text="Whilst from any new voice talent had great audio reels, the reality was not that great. When I'd give them a job, most had trouble taking direction.",
    )

    output = AUDIO_PATH / f"{id}.wav"

    sf.write(output, audio[0], 24000)

    print(
        f"[SERVICE] Omni | "
        f"Finished {id} | "
        f"{time.time()-start:.2f}s"
    )

    return {
        "audio": [str(output)]
    }
