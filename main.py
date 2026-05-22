from core.controller import TranslatorController
from gui.app import TranslatorGUI


def main():
    controller = TranslatorController()

    app = TranslatorGUI(controller)

    app.run()


if __name__ == "__main__":
    main()