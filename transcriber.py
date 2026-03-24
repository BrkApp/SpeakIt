"""Whisper transcription wrapper — loads the model once and reuses it."""

from faster_whisper import WhisperModel

import config


class Transcriber:
    """Thin wrapper around faster-whisper."""

    def __init__(self) -> None:
        self.model: WhisperModel | None = None

    def load_model(self) -> None:
        """Load the Whisper model into memory (call once at startup)."""
        print(f"Loading Whisper model '{config.WHISPER_MODEL}' (compute_type={config.COMPUTE_TYPE})…")
        self.model = WhisperModel(
            config.WHISPER_MODEL,
            device="cpu",
            compute_type=config.COMPUTE_TYPE,
        )
        print("Model loaded.")

    def transcribe(self, audio_data) -> str:
        """Transcribe a numpy float32 audio array and return the text.

        Parameters
        ----------
        audio_data : numpy.ndarray
            Mono 16 kHz float32 audio samples.

        Returns
        -------
        str
            The transcribed text, stripped of leading/trailing whitespace.
        """
        if self.model is None:
            raise RuntimeError("Model not loaded — call load_model() first.")

        segments, _info = self.model.transcribe(
            audio_data,
            language=config.WHISPER_LANGUAGE,
            beam_size=5,
            vad_filter=True,
        )
        text = " ".join(seg.text.strip() for seg in segments)
        return text.strip()
