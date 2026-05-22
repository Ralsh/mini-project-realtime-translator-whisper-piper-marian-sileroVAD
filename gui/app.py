import customtkinter as ctk

from core.queues import gui_queue


class TranslatorGUI:

    def __init__(self, controller):

        self.controller = controller

        ctk.set_appearance_mode("dark")

        self.root = ctk.CTk()

        self.root.title(
            "Realtime Voice Translator"
        )

        self.root.geometry("1000x700")

        # TOP FRAME

        self.top_frame = ctk.CTkFrame(
            self.root
        )

        self.top_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # START BUTTON

        self.start_button = ctk.CTkButton(
            self.top_frame,
            text="Start",
            command=self.start_system
        )

        self.start_button.pack(
            side="left",
            padx=5
        )

        # STOP BUTTON

        self.stop_button = ctk.CTkButton(
            self.top_frame,
            text="Stop",
            command=self.stop_system
        )

        self.stop_button.pack(
            side="left",
            padx=5
        )

        # LANGUAGE SWITCH

        self.language_var = ctk.StringVar(
            value="ru-en"
        )

        self.language_menu = (
            ctk.CTkOptionMenu(
                self.top_frame,
                values=[
                    "ru-en",
                    "en-ru"
                ],
                variable=self.language_var,
                command=self.change_language
            )
        )

        self.language_menu.pack(
            side="left",
            padx=5
        )

        # TTS SWITCH

        self.tts_var = ctk.BooleanVar(
            value=True
        )

        self.tts_switch = ctk.CTkSwitch(
            self.top_frame,
            text="TTS",
            variable=self.tts_var,
            command=self.toggle_tts
        )

        self.tts_switch.pack(
            side="left",
            padx=5
        )

        # TEXT AREA FRAME

        self.text_frame = ctk.CTkFrame(
            self.root
        )

        self.text_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # ORIGINAL TEXT

        self.original_textbox = (
            ctk.CTkTextbox(
                self.text_frame,
                width=450
            )
        )

        self.original_textbox.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # TRANSLATED TEXT

        self.translated_textbox = (
            ctk.CTkTextbox(
                self.text_frame,
                width=450
            )
        )

        self.translated_textbox.pack(
            side="right",
            fill="both",
            expand=True,
            padx=5,
            pady=5
        )

        # START GUI EVENT LOOP

        self.update_gui()

    def start_system(self):

        self.controller.start()

    def stop_system(self):

        self.controller.stop()

    def change_language(
        self,
        direction
    ):

        self.controller.set_translation_direction(
            direction
        )

    def toggle_tts(self):

        self.controller.enable_tts(
            self.tts_var.get()
        )

    def update_gui(self):

        while not gui_queue.empty():

            event = gui_queue.get()

            event_type = event.get("type")

            if event_type == "original_text":

                text = event.get("text")

                self.original_textbox.insert(
                    "end",
                    text + "\n"
                )

            elif event_type == (
                "translated_text"
            ):

                text = event.get("text")

                self.translated_textbox.insert(
                    "end",
                    text + "\n"
                )

        self.root.after(
            100,
            self.update_gui
        )

    def run(self):

        self.root.mainloop()