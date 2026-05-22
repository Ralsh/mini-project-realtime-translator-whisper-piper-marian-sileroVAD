# =========================
# AUDIO SETTINGS
# =========================

SAMPLE_RATE = 16000

CHUNK_SIZE = 512

CHANNELS = 1


# =========================
# VAD SETTINGS
# =========================

VAD_MODEL_PATH = (
    "models/silero_vad.jit"
)

VAD_THRESHOLD = 0.5

SILENCE_LIMIT = 20


# =========================
# WHISPER SETTINGS
# =========================

WHISPER_MODEL_SIZE = "base"

WHISPER_DEVICE = "cpu"

WHISPER_COMPUTE_TYPE = "int8"

WHISPER_LANGUAGE = "ru"


# =========================
# TRANSLATION SETTINGS
# =========================

DEFAULT_DIRECTION = "ru-en"

TRANSLATION_MODELS = {

    "ru-en": (
        "Helsinki-NLP/opus-mt-ru-en"
    ),

    "en-ru": (
        "Helsinki-NLP/opus-mt-en-ru"
    )
}


# =========================
# PIPER SETTINGS
# =========================

PIPER_MODEL_PATH = (
    "models/ru_RU-ruslan-medium.onnx"
)

PIPER_CONFIG_PATH = (
    "models/ru_RU-ruslan-medium.onnx.json"
)


# =========================
# GUI SETTINGS
# =========================

WINDOW_WIDTH = 1000

WINDOW_HEIGHT = 700

THEME = "dark"