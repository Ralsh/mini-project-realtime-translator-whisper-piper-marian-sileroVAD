import os
from transformers import MarianMTModel, MarianTokenizer
from core.queues import text_queue, translated_queue, gui_queue

# Принудительно отключаем сетевые проверки HuggingFace
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

class MarianTranslatorWorker:
    def __init__(self):
        self.models = {}
        self.tokenizers = {}
        self.current_direction = "ru-en"

        # Указываем локальные пути к моделям
        self.model_paths = {
            "ru-en": "./models/opus-mt-ru-en",
            "en-ru": "./models/opus-mt-en-ru"
        }

        self._load_models()

    def _load_models(self):
        for direction, path in self.model_paths.items():
            print(f"[Translator] Загрузка модели {direction} из {path}...")
            try:
                self.tokenizers[direction] = MarianTokenizer.from_pretrained(
                    path, local_files_only=True
                )
                self.models[direction] = MarianMTModel.from_pretrained(
                    path, local_files_only=True
                )
                print(f"[Translator] Модель {direction} успешно загружена в RAM.")
            except Exception as e:
                print(f"[ERROR] Не удалось загрузить модель {direction}: {e}")
                print("💡 Убедитесь, что модели скачаны в папку ./models/ с помощью huggingface-cli")

    def set_direction(self, direction):
        if direction in self.models:
            self.current_direction = direction
            print(f"[Translator] Направление переключено на {direction}")

    def translate(self, text):
        if not text.strip():
            return ""

        tokenizer = self.tokenizers[self.current_direction]
        model = self.models[self.current_direction]

        inputs = tokenizer(text, return_tensors="pt", padding=True)
        translated = model.generate(**inputs)
        result = tokenizer.decode(translated[0], skip_special_tokens=True)
        return result

    def run(self):
        while True:
            text = text_queue.get()
            translated_text = self.translate(text)
            translated_queue.put(translated_text)
            gui_queue.put({"type": "translated_text", "text": translated_text})