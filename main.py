import logging
import sys

from PyQt6.QtWidgets import QApplication, QStackedWidget
from core.launcher import Launcher


def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Инициализация приложения началась...")

    app = QApplication(sys.argv)

    # Создаем стек виджетов
    stacked_widget = QStackedWidget()

    # Передаем stacked_widget в Launcher
    logging.info("Создание экземпляра Launcher...")
    launcher = Launcher(stacked_widget)

    logging.info("Вызов launcher.setup_ui()...")
    launcher.setup_ui()

    logging.info("Приложение успешно инициализировано.")

    # Отображаем главное окно
    stacked_widget.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()