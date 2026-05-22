from transformers import MarianMTModel
from transformers import MarianTokenizer

from core.queues import (
    text_queue,
    translated_queue,
    gui_queue
)


class MarianTranslatorWorker:

    def __init__(self):

        self.models = {}

        self.tokenizers = {}

        self.current_direction = "ru-en"

        self.load_models()

    def load_models(self):

        model_names = {

            "ru-en": "Helsinki-NLP/opus-mt-ru-en",

            "en-ru": "Helsinki-NLP/opus-mt-en-ru"
        }

        for direction, model_name in model_names.items():

            tokenizer = MarianTokenizer.from_pretrained(
                model_name
            )

            model = MarianMTModel.from_pretrained(
                model_name
            )

            self.models[direction] = model

            self.tokenizers[direction] = tokenizer

    def set_direction(self, direction):

        if direction in self.models:
            self.current_direction = direction

    def translate(self, text):

        tokenizer = self.tokenizers[
            self.current_direction
        ]

        model = self.models[
            self.current_direction
        ]

        inputs = tokenizer(
            text,
            return_tensors="pt",
            padding=True
        )

        translated = model.generate(**inputs)

        result = tokenizer.decode(
            translated[0],
            skip_special_tokens=True
        )

        return result

    def run(self):

        while True:

            text = text_queue.get()

            translated_text = self.translate(text)

            translated_queue.put(
                translated_text
            )

            gui_queue.put({
                "type": "translated_text",
                "text": translated_text
            })