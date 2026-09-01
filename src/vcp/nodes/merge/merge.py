import os

from pydub import AudioSegment

from vcp.service import clear_audio
from vcp.state import GlobalState
from vcp.utils import root, timed

MERGED_PATH = root.find() / "renderer/public/audio/audio.mp3"


@timed
def merger(state: GlobalState):
    combined = AudioSegment.empty()
    sorted_audio = sorted(
        state["audio"], key=lambda x: int(os.path.splitext(os.path.basename(x))[0])
    )
    for file in sorted_audio:
        combined += AudioSegment.from_wav(file)
    clear_audio()
    combined.export(MERGED_PATH, format="mp3")
    return {"audio": [MERGED_PATH]}
