import threading
from core.queues import (
    audio_queue, speech_queue, text_queue, translated_queue, gui_queue
)
from audio.microphone import MicrophoneStream
from vad.silero_vad import SileroVADWorker
from stt.whisper_engine import WhisperWorker
from translation.marian_translator import MarianTranslatorWorker
from tts.piper_engine import PiperTTSWorker

class TranslatorController:
    def __init__(self):
        self.running = False
        self.threads = []

        # AUDIO
        self.microphone = MicrophoneStream()

        # VAD
        self.vad_worker = SileroVADWorker(model_path="models/silero_vad.jit")

        # STT
        self.whisper_worker = WhisperWorker()

        # TRANSLATOR
        self.translator_worker = MarianTranslatorWorker()

        # TTS (пути к моделям теперь управляются внутри PiperTTSWorker)
        self.tts_worker = PiperTTSWorker()

    def start(self):
        if self.running:
            return

        self.running = True
        print("Starting translator system...")

        self.microphone.start()

        # Загружаем модель TTS по умолчанию (совпадает с значением в GUI)
        self.tts_worker.set_direction("ru-en")

        workers = [
            self.vad_worker.run,
            self.whisper_worker.run,
            self.translator_worker.run,
            self.tts_worker.run
        ]

        for worker in workers:
            thread = threading.Thread(target=worker, daemon=True)
            thread.start()
            self.threads.append(thread)

    def stop(self):
        if not self.running:
            return

        self.running = False
        print("Stopping translator system...")
        self.microphone.stop()

    def set_translation_direction(self, direction):
        self.translator_worker.set_direction(direction)
        # Переключаем модель TTS синхронно с направлением перевода
        self.tts_worker.set_direction(direction)

    def enable_tts(self, enabled):
        self.tts_worker.set_enabled(enabled)