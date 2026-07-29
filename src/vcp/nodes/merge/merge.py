import os
import time
from pydub import AudioSegment

from vcp.utils import root
from vcp.state import GlobalState
from vcp.service import clear_audio


MERGED_PATH = root.find() / "src/vcp/output/final.mp3"


def merger(state: GlobalState):
    start = time.time()
    print(f"[TOOL] merger | Started merging...")

    combined = AudioSegment.empty()

    sorted_audio = sorted(
        state["audio"],
        key=lambda x: int(os.path.splitext(os.path.basename(x))[0])
    )

    for file in sorted_audio:
        combined += AudioSegment.from_wav(file)
    
    clear_audio()
    combined.export(MERGED_PATH, format="mp3")

    print(f"Merger: {time.time()-start:.2f}s")
    print(f"[TOOL] merger | Merged")

    return {"audio": [MERGED_PATH]}
