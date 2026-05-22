import torch
import numpy as np
import os

from core.queues import (
    audio_queue,
    speech_queue
)


class SileroVADWorker:

    def __init__(
        self,
        model_path,
        threshold=0.5,
        silence_limit=20
    ):

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"VAD model not found: {model_path}"
            )

        self.model = torch.jit.load(model_path)
        self.model.eval()

        self.threshold = threshold

        self.silence_limit = silence_limit

        self.speech_buffer = []

        self.speaking = False

        self.silence_chunks = 0

    def is_speech(self, audio_chunk):

        audio_tensor = torch.from_numpy(
            audio_chunk
        ).float()

        with torch.no_grad():

            speech_prob = self.model(
                audio_tensor,
                16000
            ).item()

        return speech_prob > self.threshold

    def process_chunk(self, chunk):

        if self.is_speech(chunk):

            self.speaking = True

            self.silence_chunks = 0

            self.speech_buffer.append(chunk)

        else:

            if self.speaking:

                self.silence_chunks += 1

                self.speech_buffer.append(chunk)

                if self.silence_chunks >= self.silence_limit:

                    full_speech = np.concatenate(
                        self.speech_buffer
                    )

                    speech_queue.put(full_speech)

                    self.speech_buffer.clear()

                    self.silence_chunks = 0

                    self.speaking = False

    def run(self):

        while True:

            chunk = audio_queue.get()

            self.process_chunk(chunk)