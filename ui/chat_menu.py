import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                             QHBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt
from utils.json_utils import load_json, save_json


class ChatMenu(QWidget):
    def __init__(self, switch_to, is_admin=False):
        super().__init__()
        self.switch_to = switch_to
        self.is_admin = is_admin  # Флаг администратора
        self.chats_file = "data/chats.json"  # Путь к JSON-файлу с чатами
        self.init_ui()
        self.load_chats()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(30, 30, 30, 30)

        # Заголовок
        self.title = QLabel("Чаты")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        self.layout.addWidget(self.title)

        # Контейнер для списка чатов
        self.chats_container = QWidget()
        self.chats_layout = QVBoxLayout()
        self.chats_container.setLayout(self.chats_layout)
        self.layout.addWidget(self.chats_container)

        # Кнопка "Назад"
        self.back_btn = QPushButton("Назад")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(180, 70, 70, 0.85);
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 6px;
                border: 1px solid #B22222;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: rgba(200, 90, 90, 0.9);
            }
        """)
        self.back_btn.clicked.connect(lambda: self.switch_to("main"))
        self.layout.addWidget(self.back_btn)

        # Кнопка "Добавить чат" (только для админа)
        if self.is_admin:
            self.add_btn = QPushButton("Добавить чат")
            self.add_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(100, 180, 100, 0.85);
                    color: white;
                    font-size: 16px;
                    padding: 12px;
                    border-radius: 6px;
                    border: 1px solid #64B464;
                    margin-top: 10px;
                }
                QPushButton:hover {
                    background-color: rgba(120, 200, 120, 0.9);
                }
            """)
            self.add_btn.clicked.connect(self.add_chat_dialog)
            self.layout.addWidget(self.add_btn)

        self.setLayout(self.layout)

    def load_chats(self):
        """Загрузка чатов из JSON-файла"""
        chats = load_json(self.chats_file) or []

        # Очищаем текущий список чатов
        for i in reversed(range(self.chats_layout.count())):
            item = self.chats_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        # Добавляем чаты
        if not chats:
            self.show_info_message("Информация", "Список чатов пуст!")
        for chat in chats:
            self.add_chat_button(chat)

    def add_chat_button(self, chat):
        """Добавляет кнопку чата в интерфейс"""
        chat_name = chat.get("name", "Без имени")
        chat_button = QPushButton(chat_name)
        chat_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(70, 130, 180, 0.85);
                color: white;
                font-size: 16px;
                padding: 12px;
                border-radius: 6px;
                border: 1px solid #4682B4;
                text-align: left;
                padding-left: 15px;
            }
            QPushButton:hover {
                background-color: rgba(90, 150, 200, 0.9);
            }
        """)
        chat_button.clicked.connect(lambda: self.open_chat(chat))
        self.chats_layout.addWidget(chat_button)

    def open_chat(self, chat):
        """Открывает чат (заглушка)"""
        self.show_info_message("Чат", f"Открыт чат: {chat.get('name', 'Без имени')}")

    def add_chat_dialog(self):
        """Диалог добавления нового чата"""
        chats = load_json(self.chats_file) or []
        new_chat = {"id": len(chats) + 1, "name": "Новый чат"}
        chats.append(new_chat)
        save_json(self.chats_file, chats)
        self.load_chats()

    def show_info_message(self, title, message):
        """Показать информационное сообщение"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()