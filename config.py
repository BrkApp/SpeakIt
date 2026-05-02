"""Configuration for the voice dictation application."""

# Whisper model settings
WHISPER_MODEL = "whisper-base-model"   # Local path to model directory
WHISPER_LANGUAGE = "fr"                # Language code (e.g., "fr", "en")
COMPUTE_TYPE = "float32"              # "float32" for CPU compatibility

# Hotkey
HOTKEY = "ctrl+space"

# Audio settings
SAMPLE_RATE = 16000             # Whisper expects 16kHz
CHANNELS = 1                    # Mono audio
AUDIO_DEVICE = None             # None = system default microphone

# Auto-punctuation
AUTO_PUNCTUATE = True           # Add basic punctuation to transcriptions

# Transcription log
LOG_FILE = "transcription_log.txt"
ENABLE_LOG = True

# Auto-start
AUTO_START = False              # Start with Windows (registry)
