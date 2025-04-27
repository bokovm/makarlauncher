import logging
import sys

from PyQt6.QtWidgets import QApplication, QStackedWidget, QMessageBox
from core.launcher import Launcher


def main():
    try:
        app = QApplication(sys.argv)
        stacked_widget = QStackedWidget()
        launcher = Launcher(stacked_widget)
        launcher.show()
        sys.exit(app.exec())
    except Exception as e:
        logging.critical(f"Критическая ошибка: {e}", exc_info=True)
        QMessageBox.critical(None, "Ошибка", f"Программа завершена из-за ошибки:\n{str(e)}")
        sys.exit(1)

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