import os
import sys
import zipfile
import shutil
import requests
from PyQt6.QtWidgets import QProgressDialog, QMessageBox, QFileDialog
from PyQt6.QtCore import Qt, QThread, pyqtSignal


class UpdateManager(QThread):
    """Класс для управления процессом обновлений"""
    progress_updated = pyqtSignal(int)
    update_finished = pyqtSignal(bool, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.update_url = "https://your-update-server.com/api/check-update"
        self.current_version = "1.0.0"
        self.temp_dir = "temp_update"
        self.update_info = None

    def check_for_updates(self):
        """Проверка наличия обновлений на сервере"""
        try:
            response = requests.get(
                self.update_url,
                params={"version": self.current_version},
                timeout=10
            )
            response.raise_for_status()
            self.update_info = response.json()
            return True
        except Exception as e:
            print(f"Ошибка проверки обновлений: {e}")
            return False

    def download_update(self):
        """Загрузка обновления с сервера"""
        if not self.update_info:
            return False

        try:
            os.makedirs(self.temp_dir, exist_ok=True)
            url = self.update_info['download_url']

            with requests.get(url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                downloaded = 0

                with open(os.path.join(self.temp_dir, "update.zip"), 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        progress = int((downloaded / total_size) * 100)
                        self.progress_updated.emit(progress)

            return True
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            return False

    def apply_update(self):
        """Применение обновления"""
        try:
            zip_path = os.path.join(self.temp_dir, "update.zip")

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(self.temp_dir)

            content_dir = os.path.join(self.temp_dir, "content")
            if os.path.exists(content_dir):
                for item in os.listdir(content_dir):
                    src = os.path.join(content_dir, item)
                    dst = os.path.join(".", item)

                    if os.path.isdir(src):
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src, dst)

            shutil.rmtree(self.temp_dir)
            return True
        except Exception as e:
            print(f"Ошибка установки: {e}")
            return False

    def run(self):
        """Основной метод выполнения обновления"""
        success = False
        message = "Обновление успешно установлено"

        try:
            if not self.check_for_updates():
                self.update_finished.emit(False, "Не удалось проверить обновления")
                return

            if not self.update_info['update_available']:
                self.update_finished.emit(False, "У вас актуальная версия")
                return

            if not self.download_update():
                self.update_finished.emit(False, "Ошибка загрузки обновления")
                return

            if not self.apply_update():
                self.update_finished.emit(False, "Ошибка установки обновления")
                return

            success = True
        except Exception as e:
            message = f"Ошибка: {str(e)}"

        self.update_finished.emit(success, message)


class UpdateDialog:
    """Диалоговое окно для управления обновлениями"""

    def __init__(self, parent):
        self.parent = parent
        self.manager = UpdateManager()
        self.manager.progress_updated.connect(self.update_progress)
        self.manager.update_finished.connect(self.update_completed)

        self.progress_dialog = QProgressDialog(
            "Проверка обновлений...",
            "Отмена",
            0,
            100,
            parent
        )
        self.progress_dialog.setWindowTitle("Обновление лаунчера")
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.canceled.connect(self.cancel_update)

    def check_and_install(self):
        """Запуск процесса обновления"""
        self.progress_dialog.show()
        self.manager.start()

    def update_progress(self, value):
        """Обновление прогресса"""
        self.progress_dialog.setValue(value)
        self.progress_dialog.setLabelText(
            "Загрузка обновления..." if value < 50
            else "Установка обновления..."
        )

    def update_completed(self, success, message):
        """Завершение процесса обновления"""
        self.progress_dialog.close()

        msg = QMessageBox(self.parent)
        msg.setWindowTitle("Результат обновления")
        msg.setText(message)
        msg.setIcon(QMessageBox.Icon.Information if success else QMessageBox.Icon.Warning)

        if success:
            msg.buttonClicked.connect(self.restart_application)

        msg.exec()

    def cancel_update(self):
        """Отмена обновления"""
        if self.manager.isRunning():
            self.manager.terminate()

        QMessageBox.information(
            self.parent,
            "Обновление отменено",
            "Процесс обновления был прерван"
        )

    @staticmethod
    def restart_application():
        """Перезапуск приложения"""
        from PyQt6.QtWidgets import QApplication
        QApplication.instance().quit()
        os.execl(sys.executable, sys.executable, *sys.argv)


def install_local_update(file_path, parent_window=None):
    """Установка обновления из локального файла"""
    try:
        if not os.path.exists(file_path):
            QMessageBox.warning(parent_window, "Ошибка", "Файл обновления не найден")
            return False

        if not zipfile.is_zipfile(file_path):
            QMessageBox.warning(parent_window, "Ошибка", "Неверный формат файла (требуется ZIP)")
            return False

        temp_dir = "temp_update"
        os.makedirs(temp_dir, exist_ok=True)

        try:
            shutil.copy(file_path, os.path.join(temp_dir, "update.zip"))

            manager = UpdateManager()
            manager.temp_dir = temp_dir
            manager.update_info = {"update_available": True}

            if manager.apply_update():
                QMessageBox.information(
                    parent_window,
                    "Успех",
                    "Обновление установлено. Приложение будет перезапущено."
                )
                UpdateDialog.restart_application()
                return True
            else:
                QMessageBox.critical(
                    parent_window,
                    "Ошибка",
                    "Не удалось установить обновление"
                )
                return False
        finally:
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)

    except Exception as e:
        QMessageBox.critical(
            parent_window,
            "Ошибка",
            f"Произошла ошибка: {str(e)}"
        )
        return False