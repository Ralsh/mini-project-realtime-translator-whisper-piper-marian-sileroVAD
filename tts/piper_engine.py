import os
import numpy as np
import sounddevice as sd

from pathlib import Path

from piper import PiperVoice

from core.queues import (
    translated_queue,
    gui_queue
)


class PiperTTSWorker:

    def __init__(
        self,
        model_path,
        config_path
    ):

        if not Path(model_path).exists():
            raise FileNotFoundError(
                f"Piper model not found: {model_path}"
            )

        self.voice = PiperVoice.load(
            model_path,
            config_path=config_path
        )

        self.enabled = True

    def set_enabled(self, enabled):

        self.enabled = enabled

    def synthesize(self, text):

        chunks = list(
            self.voice.synthesize(text)
        )

        if not chunks:
            return None, None

        audio_np = np.concatenate([
            chunk.audio_float_array
            for chunk in chunks
        ])

        sample_rate = chunks[0].sample_rate

        return audio_np, sample_rate

    def play_audio(
        self,
        audio_data,
        sample_rate
    ):

        sd.play(audio_data, sample_rate)

    def run(self):

        while True:

            text = translated_queue.get()

            if not self.enabled:
                continue

            audio_data, sample_rate = (
                self.synthesize(text)
            )

            if audio_data is None:
                continue

            self.play_audio(
                audio_data,
                sample_rate
            )

            gui_queue.put({
                "type": "tts_finished"
            })