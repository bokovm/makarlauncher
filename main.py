import logging

from PyQt6.QtWidgets import QApplication, QStackedWidget
from core.launcher import Launcher
import sys


def main():
    logging.info("Инициализация приложения началась...")
    """Главная функция для запуска приложения"""
    print("Инициализация приложения...")
    app = QApplication(sys.argv)

    # Создаём стек виджетов
    stacked_widget = QStackedWidget()

    # Передаём stacked_widget в Launcher
    logging.info("Создание экземпляра Launcher...")
    launcher = Launcher(stacked_widget)

    logging.info("Вызов launcher.setup_ui()...")
    launcher.setup_ui()

    logging.info("Приложение успешно инициализировано.")

    # Отображаем окно
    stacked_widget.show()

    sys.exit(app.exec())

    app.exec()
    logging.info("Приложение завершено.")

if __name__ == "__main__":
    main()