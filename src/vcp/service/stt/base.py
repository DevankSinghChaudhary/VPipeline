import gc

import torch
import whisperx


class WhisperX:
    LANGUAGE = "en"

    def __init__(
        self,
        device: str = "cuda",
        model_name: str = "medium",
        compute_type: str = "float16",
        batch_size: int = 4,
    ):
        self.device = device
        self.model_name = model_name
        self.compute_type = compute_type
        self.batch_size = batch_size

        self.asr_model = None
        self.align_model = None
        self.align_metadata = None

    def load_asr(self):
        self.asr_model = whisperx.load_model(
            self.model_name,
            self.device,
            compute_type=self.compute_type,
        )

    def transcribe(self, audio_path: str):
        if self.asr_model is None:
            raise RuntimeError("ASR model is not loaded.")

        audio = whisperx.load_audio(audio_path)

        result = self.asr_model.transcribe(
            audio,
            batch_size=self.batch_size,
            language=self.LANGUAGE,
        )

        return audio, result

    def load_alignment(self):
        self.align_model, self.align_metadata = whisperx.load_align_model(
            language_code=self.LANGUAGE,
            device=self.device,
        )

    def align(self, segments, audio):
        if self.align_model is None or self.align_metadata is None:
            raise RuntimeError("Alignment model is not loaded.")

        result = whisperx.align(
            segments,
            self.align_model,
            self.align_metadata,
            audio,
            self.device,
            return_char_alignments=False,
        )

        return self._normalize_result(result)

    def transcribe_and_align(self, audio_path: str):
        """
        Transcribe one audio file and produce normalized word-level timestamps.

        Returns:
            audio: decoded audio array
            result: normalized WhisperX aligned result
        """
        audio, result = self.transcribe(audio_path)

        aligned = self.align(
            result["segments"],
            audio,
        )

        return audio, aligned

    @staticmethod
    def _normalize_result(result):
        """
        Convert NumPy scalar values returned by WhisperX into
        native Python types so the result is cleanly serializable.
        """
        for segment in result.get("segments", []):
            if "start" in segment:
                segment["start"] = float(segment["start"])

            if "end" in segment:
                segment["end"] = float(segment["end"])

            for word in segment.get("words", []):
                WhisperX._normalize_word(word)

        for word in result.get("word_segments", []):
            WhisperX._normalize_word(word)

        return result

    @staticmethod
    def _normalize_word(word):
        if "start" in word:
            word["start"] = float(word["start"])

        if "end" in word:
            word["end"] = float(word["end"])

        if "score" in word:
            word["score"] = float(word["score"])

        if "word" in word:
            word["word"] = str(word["word"]).strip()

    def unload_asr(self):
        self.asr_model = None
        self._clear_cuda()

    def unload_alignment(self):
        self.align_model = None
        self.align_metadata = None
        self._clear_cuda()

    def unload(self):
        self.asr_model = None
        self.align_model = None
        self.align_metadata = None

        self._clear_cuda()

    def _clear_cuda(self):
        gc.collect()

        if self.device == "cuda" and torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()
