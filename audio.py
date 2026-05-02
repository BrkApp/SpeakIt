"""Audio capture module — records from microphone in a separate thread."""

import threading
import numpy as np
import sounddevice as sd

import config


class AudioRecorder:
    """Non-blocking microphone recorder that accumulates audio chunks."""

    def __init__(self):
        self._lock = threading.Lock()
        self._chunks: list[np.ndarray] = []
        self._stream: sd.InputStream | None = None
        self.is_recording = False

    # -- public API ----------------------------------------------------------

    def start(self) -> None:
        """Start capturing audio from the microphone."""
        with self._lock:
            if self.is_recording:
                return
            self._chunks.clear()
            self._stream = sd.InputStream(
                samplerate=config.SAMPLE_RATE,
                channels=config.CHANNELS,
                dtype="float32",
                device=config.AUDIO_DEVICE,
                callback=self._audio_callback,
            )
            self._stream.start()
            self.is_recording = True

    def stop(self) -> np.ndarray | None:
        """Stop recording and return the captured audio as a float32 numpy array.

        Returns ``None`` when there is nothing recorded.
        """
        with self._lock:
            if not self.is_recording:
                return None
            self.is_recording = False
            if self._stream is not None:
                self._stream.stop()
                self._stream.close()
                self._stream = None
            if not self._chunks:
                return None
            audio = np.concatenate(self._chunks, axis=0).flatten()
            self._chunks.clear()
            return audio

    def cleanup(self) -> None:
        """Release microphone resources."""
        self.stop()

    # -- internals -----------------------------------------------------------

    def _audio_callback(self, indata: np.ndarray, frames, time_info, status) -> None:  # noqa: ANN001
        """sounddevice callback — runs in a separate audio thread."""
        self._chunks.append(indata.copy())
