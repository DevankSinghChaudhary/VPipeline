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

    engine.unload()
    try:
        engine.load_asr()
        engine.load_alignment()

        for audio_path in state["audio"]:
            print(f"[whisperx_engine] Processing scene {audio_path}")

            audio_data, result = engine.transcribe_and_align(audio_path)

            transcriptions.append(
                {
                    "audio": audio_data,
                    "result": result,
                }
            )

    finally:
        engine.unload()

    return {"stt": transcriptions}
