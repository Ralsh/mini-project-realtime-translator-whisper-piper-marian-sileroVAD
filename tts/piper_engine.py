import threading
import numpy as np
import sounddevice as sd
from pathlib import Path
from piper import PiperVoice
from core.queues import translated_queue, gui_queue


class PiperTTSWorker:
    def __init__(self):
        self.voice = None
        self.enabled = True
        self.lock = threading.Lock()  # Для потокобезопасной замены модели

        # Словарь соответствия направлений и путей к моделям
        self.model_config = {
            "ru-en": {
                "model": "models/ru_RU-ruslan-medium.onnx",
                "config": "models/ru_RU-ruslan-medium.onnx.json"
            },
            "en-ru": {
                "model": "models/en_US-bryce-medium.onnx",
                "config": "models/en_US-bryce-medium.onnx.json"
            }
        }

    def set_enabled(self, enabled):
        self.enabled = enabled

    def set_direction(self, direction):
        """Динамически загружает модель TTS для выбранного направления."""
        if direction not in self.model_config:
            raise ValueError(f"Неподдерживаемое направление: {direction}")

        cfg = self.model_config[direction]
        if not Path(cfg["model"]).exists() or not Path(cfg["config"]).exists():
            raise FileNotFoundError(f"Файлы модели или конфига для {direction} не найдены")

        with self.lock:
            self.voice = PiperVoice.load(cfg["model"], config_path=cfg["config"])
            print(f"[TTS] Модель переключена на: {direction}")

    def synthesize(self, text):
        with self.lock:
            if self.voice is None:
                return None, None
            chunks = list(self.voice.synthesize(text))

        if not chunks:
            return None, None

        audio_np = np.concatenate([chunk.audio_float_array for chunk in chunks])
        sample_rate = chunks[0].sample_rate
        return audio_np, sample_rate

    def play_audio(self, audio_data, sample_rate):
        sd.play(audio_data, sample_rate)
        sd.wait()  # Ждём окончания воспроизведения, чтобы избежать наложения аудио

    def run(self):
        while True:
            text = translated_queue.get()

            if not self.enabled or self.voice is None:
                continue

            audio_data, sample_rate = self.synthesize(text)
            if audio_data is None:
                continue

            self.play_audio(audio_data, sample_rate)
            gui_queue.put({"type": "tts_finished"})