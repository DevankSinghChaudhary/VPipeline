from pathlib import Path

from vcp.state import global_state
from vcp.utils import timed

from .base import WhisperX


@timed
def whisperx_engine(state: global_state):
    engine = WhisperX(
        device="cuda",
        model_name="small",
        compute_type="float",
        batch_size=4,
    )
    transcriptions = []

    # Unloading engine for tts to clear out vram for stt
    engine.unload()

    try:
        engine.load_asr()
        engine.load_alignment()

        for audio_path in state["audio"]:
            audio_id = int(Path(audio_path).stem)
            print(f"[whisperx_engine] Processing audio {audio_id}")

            audio_data, result = engine.transcribe_and_align(audio_path)

            transcriptions.append(
                {
                    "path": audio_path,
                    "audio_id": audio_id,
                    "result": result,
                }
            )

    finally:
        engine.unload()

    return {"stt": transcriptions}
