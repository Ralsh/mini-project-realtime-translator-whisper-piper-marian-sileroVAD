import sounddevice as sd
import numpy as np

from core.queues import audio_queue


class MicrophoneStream:

    def __init__(
        self,
        sample_rate=16000,
        chunk_size=512
    ):

        self.sample_rate = sample_rate
        self.chunk_size = chunk_size

        self.stream = None

    def audio_callback(self, indata, frames, time, status):

        if status:
            return

        audio_chunk = indata.copy().flatten()

        audio_queue.put(audio_chunk)

    def start(self):

        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype=np.float32,
            blocksize=self.chunk_size,
            callback=self.audio_callback
        )

        self.stream.start()

    def stop(self):

        if self.stream:
            self.stream.stop()
            self.stream.close()