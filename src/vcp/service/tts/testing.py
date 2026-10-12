import time

import soundfile as sf
import torch
from omnivoice import OmniVoice

AUDIO_PATH = "/home/devank/Projects/tts/1.wav"


def omni():

    start = time.time()
    text = "Scientists study [EH2 K S OW0 P L AE1 N AH0 T], [G AE1 L AH0 K S IY0], [K AH0 M P Y UW1 T ER0], and [S P EY1 S K R AE2 F T] to understand our universe."

    print("[SERVICE] Omni | Generating 1...")

    model = OmniVoice.from_pretrained(
        "k2-fsa/OmniVoice", device_map="cuda:0", dtype=torch.float16
    )
    audio = model.generate(
        text=text,
        ref_audio="/home/devank/Projects/VPipeline/src/vcp/service/tts/assets/ref.mp3",
        ref_text="The McLaren 720S demonstrates exceptional aerodynamic efficiency with its 4.0-liter twin-turbocharged V8 engine",
    )

    print(f"[SERVICE] Omni | Finished {id} | {time.time() - start:.2f}s")

    sf.write(AUDIO_PATH, audio[0], 24000)

    return str(AUDIO_PATH)


print(omni())
