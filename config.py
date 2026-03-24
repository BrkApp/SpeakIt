"""Configuration for the voice dictation application."""

# Whisper model settings
WHISPER_MODEL = "base"          # "tiny", "base", or "small"
WHISPER_LANGUAGE = "fr"         # Language code (e.g., "fr", "en")
COMPUTE_TYPE = "int8"           # "int8" for CPU, "float16" for GPU

# Hotkey
HOTKEY = "ctrl+space"

# Audio settings
SAMPLE_RATE = 16000             # Whisper expects 16kHz
CHANNELS = 1                    # Mono audio
AUDIO_DEVICE = None             # None = system default microphone

# Transcription log
LOG_FILE = "transcription_log.txt"
ENABLE_LOG = True
