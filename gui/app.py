import customtkinter as ctk
from core.queues import gui_queue
import os
os.environ["HF_HUB_OFFLINE"] = "1"  # Отключает все сетевые проверки HF
os.environ["TRANSFORMERS_OFFLINE"] = "1"

class TranslatorGUI:
    def __init__(self, controller):
        self.controller = controller

        # Глобальные настройки темы
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = ctk.CTk()
        self.root.title("Realtime Voice Translator")
        self.root.geometry("1100x750")
        self.root.resizable(True, True)

        # Переменные состояния
        self.language_var = ctk.StringVar(value="ru-en")
        self.tts_var = ctk.BooleanVar(value=True)
        self.status_var = ctk.StringVar(value="⏹️ Готов к работе")

        # Сборка интерфейса
        self._build_header()
        self._build_control_panel()
        self._build_text_area()

        # Запуск цикла обновления GUI
        self.update_gui()

    def _build_header(self):
        self.header_frame = ctk.CTkFrame(self.root, fg_color=("gray20", "gray15"), corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="🎙️ Realtime Voice Translator",
            font=ctk.CTkFont(size=26, weight="bold", family="Segoe UI")
        )
        self.title_label.pack(side="left", padx=25, pady=18)

        self.status_label = ctk.CTkLabel(
            self.header_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=16, weight="normal"),
            text_color="#88ccff"
        )
        self.status_label.pack(side="right", padx=25, pady=18)

    def _build_control_panel(self):
        self.control_frame = ctk.CTkFrame(self.root, fg_color=("gray25", "gray20"), corner_radius=12)
        self.control_frame.pack(fill="x", padx=20, pady=(15, 10))

        self.start_btn = ctk.CTkButton(
            self.control_frame, text="▶️ Старт", command=self.start_system,
            font=ctk.CTkFont(size=14, weight="bold"), fg_color="#2ecc71", hover_color="#27ae60", width=110
        )
        self.start_btn.grid(row=0, column=0, padx=12, pady=10, sticky="ew")

        self.stop_btn = ctk.CTkButton(
            self.control_frame, text="⏹️ Стоп", command=self.stop_system,
            font=ctk.CTkFont(size=14, weight="bold"), fg_color="#e74c3c", hover_color="#c0392b", width=110
        )
        self.stop_btn.grid(row=0, column=1, padx=12, pady=10, sticky="ew")

        ctk.CTkLabel(self.control_frame, text="Направление:", font=ctk.CTkFont(size=14)).grid(row=0, column=2, padx=10,
                                                                                              pady=10)

        self.language_menu = ctk.CTkOptionMenu(
            self.control_frame, variable=self.language_var, values=["ru-en", "en-ru"],
            command=self.change_language, width=130, font=ctk.CTkFont(size=14)
        )
        self.language_menu.grid(row=0, column=3, padx=10, pady=10)

        self.tts_switch = ctk.CTkSwitch(
            self.control_frame, text="🔊 Озвучка (TTS)", variable=self.tts_var,
            command=self.toggle_tts, font=ctk.CTkFont(size=14)
        )
        self.tts_switch.grid(row=0, column=4, padx=15, pady=10)

        # Равномерное распределение элементов
        self.control_frame.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)

    def _build_text_area(self):
        self.text_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.text_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Настройка сетки для текстовых полей
        self.text_frame.grid_rowconfigure(1, weight=1)
        self.text_frame.grid_columnconfigure(0, weight=1)
        self.text_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(self.text_frame, text="📝 Исходный текст", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0,
                                                                                                              column=0,
                                                                                                              padx=5,
                                                                                                              pady=(0,
                                                                                                                    8),
                                                                                                              sticky="sw")
        self.original_textbox = ctk.CTkTextbox(self.text_frame, font=ctk.CTkFont(size=14, family="Consolas"),
                                               corner_radius=10)
        self.original_textbox.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        ctk.CTkLabel(self.text_frame, text="🌐 Перевод", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=1,
                                                                                                       padx=5,
                                                                                                       pady=(0, 8),
                                                                                                       sticky="sw")
        self.translated_textbox = ctk.CTkTextbox(self.text_frame, font=ctk.CTkFont(size=14, family="Consolas"),
                                                 corner_radius=10)
        self.translated_textbox.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

    def start_system(self):
        self.controller.start()
        self.status_var.set("🎧 Слушаю и перевожу...")

    def stop_system(self):
        self.controller.stop()
        self.status_var.set("⏹️ Готов к работе")

    def change_language(self, direction):
        self.controller.set_translation_direction(direction)

    def toggle_tts(self):
        self.controller.enable_tts(self.tts_var.get())

    def update_gui(self):
        while not gui_queue.empty():
            event = gui_queue.get()
            event_type = event.get("type")

            if event_type == "original_text":
                text = event.get("text")
                self.original_textbox.insert("end", text + "\n")
                self.original_textbox.see("end")  # Автопрокрутка вниз

            elif event_type == "translated_text":
                text = event.get("text")
                self.translated_textbox.insert("end", text + "\n")
                self.translated_textbox.see("end")  # Автопрокрутка вниз

        self.root.after(100, self.update_gui)

    def run(self):
        self.root.mainloop()