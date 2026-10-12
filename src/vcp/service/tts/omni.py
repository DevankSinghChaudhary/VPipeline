import time

import soundfile as sf
import torch
from omnivoice import OmniVoice

from vcp.state import GlobalState
from vcp.utils import root

PATH = root()

AUDIO_PATH = PATH.find("renderer/public/audio")
REF_AUDIO = str(PATH.find("src/vcp/service/tts/assets/ref.mp3"))

REF_TEXT = (
    "The McLaren 720S demonstrates exceptional aerodynamic efficiency "
    "with its 4.0-liter twin-turbocharged V8 engine"
)

model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map="cuda:0",
    dtype=torch.float16,
)


def omni(state: GlobalState):
    audio_paths = []

    for script in state["script"].script:
        start = time.perf_counter()

        print(f"[SERVICE] Omni | Generating {script.id}...")

        audio = model.generate(
            text=script.script,
            ref_audio=REF_AUDIO,
            ref_text=REF_TEXT,
        )

        output = AUDIO_PATH / f"{script.id}.wav"

        sf.write(
            output,
            audio[0],
            24000,
        )

        audio_paths.append(str(output))

        print(
            f"[SERVICE] Omni | Finished {script.id} "
            f"| {time.perf_counter() - start:.2f}s"
        )

    return {
        "audio": audio_paths,
    }
