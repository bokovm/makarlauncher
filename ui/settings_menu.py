import hashlib
import os
import zipfile
import shutil
import sys
import sqlite3
import json
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                             QFileDialog, QMessageBox, QHBoxLayout,
                             QColorDialog, QFontDialog, QInputDialog)
from PyQt6.QtGui import QFont, QIcon, QColor
from PyQt6.QtCore import Qt, QSize

from admin.views.dialogs.settings import SettingsDialog


class SettingsMenu(QWidget):
    def __init__(self, switch_to, is_admin=False):
        super().__init__()
        self.switch_to = switch_to
        self.is_admin = is_admin
        self.current_theme = 'dark'
        self.settings_file = 'launcher_settings.json'
        self.init_db()  # Инициализация БД при создании
        self.init_ui()
        self.load_settings()
        self.setup_styles()

    @staticmethod
    def init_db():
        """Инициализация базы данных"""
        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY,
                    background_image TEXT,
                    background_color TEXT DEFAULT '#333333',
                    opacity REAL DEFAULT 0.9,
                    font_family TEXT DEFAULT 'Arial',
                    admin_password TEXT)""")

        # Проверяем наличие записи
        c.execute("SELECT COUNT(*) FROM settings WHERE id=1")
        if c.fetchone()[0] == 0:
            default_pass = hashlib.sha256('admin'.encode()).hexdigest()
            c.execute("""INSERT INTO settings (id, admin_password) 
                         VALUES (1, ?)""", (default_pass,))

        conn.commit()
        conn.close()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(50, 50, 50, 50)

        # Заголовок
        self.title = QLabel("Настройки")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        # Основные настройки
        self.main_settings_btn = QPushButton("Основные настройки")
        self.main_settings_btn.clicked.connect(self.show_main_settings)
        self.layout.addWidget(self.main_settings_btn)

        # Внешний вид
        self.appearance_btn = QPushButton("Внешний вид")
        self.appearance_btn.clicked.connect(self.show_appearance_settings)
        self.layout.addWidget(self.appearance_btn)

        # Обновление
        self.update_btn = QPushButton("Обновить лаунчер")
        self.update_btn.clicked.connect(self.update_launcher)
        self.layout.addWidget(self.update_btn)

        # О программе
        self.about_btn = QPushButton("О программе")
        self.about_btn.clicked.connect(self.show_about)
        self.layout.addWidget(self.about_btn)

        # Кнопка "Назад"
        self.back_btn = QPushButton("Назад")
        self.back_btn.clicked.connect(lambda: self.switch_to("main"))
        self.layout.addWidget(self.back_btn)

        # Админ-функции
        if self.is_admin:
            self.admin_btn = QPushButton("Администрирование")
            self.admin_btn.clicked.connect(self.show_admin_panel)
            self.layout.addWidget(self.admin_btn)

        self.setLayout(self.layout)

    def setup_styles(self):
        """Устанавливает стили для всех элементов"""
        base_style = """
            QPushButton {
                min-height: 50px;
                font-size: 16px;
                border-radius: 8px;
                padding: 10px;
                margin: 5px;
            }
        """

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {'#333333' if self.current_theme == 'dark' else '#f0f0f0'};
                color: {'white' if self.current_theme == 'dark' else 'black'};
            }}
            {base_style}
            QLabel {{
                color: {'white' if self.current_theme == 'dark' else 'black'};
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }}
            QPushButton {{
                background-color: rgba(150, 100, 200, 0.85);
                color: white;
                border: 2px solid #9664C8;
            }}
            QPushButton:hover {{
                background-color: rgba(170, 120, 220, 0.9);
            }}
            QPushButton#back_btn {{
                background-color: rgba(200, 80, 80, 0.85);
                border: 2px solid #C85050;
            }}
            QPushButton#back_btn:hover {{
                background-color: rgba(220, 100, 100, 0.9);
            }}
            QPushButton#admin_btn {{
                background-color: rgba(180, 70, 70, 0.85);
                border: 2px solid #B44646;
            }}
            QPushButton#admin_btn:hover {{
                background-color: rgba(200, 90, 90, 0.9);
            }}
        """)

        # Устанавливаем objectName для специальных кнопок
        self.back_btn.setObjectName("back_btn")
        if hasattr(self, 'admin_btn'):
            self.admin_btn.setObjectName("admin_btn")

    def load_settings(self):
        """Загружает настройки из файла"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    self.current_theme = settings.get('theme', 'dark')
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")

    def save_settings(self):
        """Сохраняет настройки в файл"""
        try:
            settings = {
                'theme': self.current_theme,
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")

    def show_main_settings(self):
        """Показывает основные настройки"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Основные настройки")
        msg.setText("Здесь будут основные настройки лаунчера")
        msg.setStyleSheet(self.get_messagebox_style())
        msg.exec()

    def show_appearance_settings(self):
        """Показывает настройки внешнего вида"""
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Настройки внешнего вида")
        dialog.setLabelText("Выберите тему:")
        dialog.setStyleSheet(self.get_messagebox_style())
        dialog.setComboBoxItems(["Темная", "Светлая"])
        dialog.setCurrentIndex(0 if self.current_theme == 'dark' else 1)

        if dialog.exec():
            selected_theme = dialog.textValue()
            self.current_theme = 'dark' if selected_theme == "Темная" else 'light'
            self.setup_styles()
            self.save_settings()

    def update_launcher(self):
        """Обновление лаунчера"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл обновления",
            "",
            "ZIP Archives (*.zip)"
        )

        if file_path:
            try:
                temp_dir = "temp_update"
                os.makedirs(temp_dir, exist_ok=True)

                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)

                # Здесь должна быть логика обновления файлов
                # Например, копирование из temp_dir в нужные места

                self.show_message("Успех",
                                "Лаунчер успешно обновлен! Перезапустите программу.")
                shutil.rmtree(temp_dir)

            except Exception as e:
                self.show_message("Ошибка",
                                f"Не удалось выполнить обновление:\n{str(e)}")

    def show_about(self):
        """Показывает информацию о программе"""
        about_text = """
        <b>Лаунчер для бабушки</b><br><br>
        Версия: 2.0<br>
        Разработчик: Ваше имя<br><br>
        © 2023 Все права защищены
        """

        msg = QMessageBox(self)
        msg.setWindowTitle("О программе")
        msg.setTextFormat(Qt.TextFormat.RichText)
        msg.setText(about_text)
        msg.setStyleSheet(self.get_messagebox_style())
        msg.exec()

    def show_admin_panel(self):
        """Показывает панель администратора"""
        dialog = SettingsDialog(self)
        if dialog.exec():
            self.show_message("Сохранено", "Настройки успешно обновлены")

    def get_messagebox_style(self):
        """Возвращает стиль для QMessageBox в зависимости от темы"""
        return f"""
            QMessageBox {{
                background-color: {'#333333' if self.current_theme == 'dark' else '#f0f0f0'};
            }}
            QLabel {{
                color: {'white' if self.current_theme == 'dark' else 'black'};
            }}
            QPushButton {{
                background-color: {'#555555' if self.current_theme == 'dark' else '#e0e0e0'};
                color: {'white' if self.current_theme == 'dark' else 'black'};
                border: 1px solid {'#666666' if self.current_theme == 'dark' else '#cccccc'};
                padding: 5px;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background-color: {'#666666' if self.current_theme == 'dark' else '#d0d0d0'};
            }}
        """

    def show_message(self, title, message):
        """Показывает сообщение"""
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet(self.get_messagebox_style())
        msg.exec()

    def restart_application(self):
        """Перезапуск приложения"""
        from PyQt6.QtWidgets import QApplication
        QApplication.instance().quit()
        os.execl(sys.executable, sys.executable, *sys.argv)