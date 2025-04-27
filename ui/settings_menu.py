import os
import json
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                             QFileDialog, QMessageBox, QInputDialog)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt
from utils.json_utils import load_json, save_json


class SettingsMenu(QWidget):
    def __init__(self, switch_to, is_admin=False):
        super().__init__()
        self.switch_to = switch_to
        self.is_admin = is_admin
        self.settings_file = "data/settings.json"  # Путь к JSON файлу настроек
        self.current_theme = "dark"
        self.init_ui()
        self.load_settings()
        self.setup_styles()

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

    def load_settings(self):
        """Загрузка настроек из JSON файла"""
        settings = load_json(self.settings_file)
        if settings:
            self.current_theme = settings.get("theme", "dark")

    def save_settings(self):
        """Сохранение настроек в JSON файл"""
        settings = {
            "theme": self.current_theme,
        }
        save_json(self.settings_file, settings)

    def setup_styles(self):
        """Установка стилей на основе текущей темы"""
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {'#333333' if self.current_theme == 'dark' else '#f0f0f0'};
                color: {'white' if self.current_theme == 'dark' else 'black'};
            }}
            QPushButton {{
                background-color: rgba(150, 100, 200, 0.85);
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 8px;
                border: 2px solid #9664C8;
            }}
            QPushButton:hover {{
                background-color: rgba(170, 120, 220, 0.9);
            }}
            QLabel {{
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }}
        """)

    def show_main_settings(self):
        """Показ основных настроек"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Основные настройки")
        msg.setText("Здесь будут основные настройки лаунчера.")
        msg.exec()

    def show_appearance_settings(self):
        """Показ настроек внешнего вида"""
        dialog = QInputDialog(self)
        dialog.setWindowTitle("Настройки внешнего вида")
        dialog.setLabelText("Выберите тему:")
        dialog.setComboBoxItems(["Темная", "Светлая"])
        dialog.setCurrentIndex(0 if self.current_theme == "dark" else 1)

        if dialog.exec():
            selected_theme = dialog.textValue()
            self.current_theme = "dark" if selected_theme == "Темная" else "light"
            self.setup_styles()
            self.save_settings()

    def show_admin_panel(self):
        """Показ панели администрирования"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Администрирование")
        msg.setText("Здесь будут настройки для администраторов.")
        msg.exec()