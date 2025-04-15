import subprocess
from PyQt6.QtWidgets import QMessageBox

def safe_launch(path_or_command, parent=None):
    try:
        subprocess.Popen(path_or_command)
    except FileNotFoundError:
        show_error("Программа не найдена. Убедись, что она установлена.", parent)
    except Exception as e:
        show_error(f"Ошибка запуска: {str(e)}", parent)

def show_error(message, parent=None):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("Ошибка запуска")
    msg.setText(message)
    msg.exec()
