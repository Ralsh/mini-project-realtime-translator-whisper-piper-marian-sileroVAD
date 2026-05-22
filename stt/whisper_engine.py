from faster_whisper import WhisperModel

from core.queues import (
    speech_queue,
    text_queue,
    gui_queue
)


class WhisperWorker:

    def __init__(self):

        self.model = WhisperModel(
            model_size_or_path="base",
            device="cpu",
            compute_type="int8"
        )

    def transcribe(self, audio_data):

        segments, info = self.model.transcribe(
            audio_data,
            language="ru",
            beam_size=1
        )

        text = ""

        for segment in segments:
            text += segment.text

        return text.strip()

    def run(self):

        while True:

            audio_data = speech_queue.get()

            text = self.transcribe(audio_data)

            if text:

                text_queue.put(text)

                gui_queue.put({
                    "type": "original_text",
                    "text": text
                })