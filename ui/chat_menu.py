import os

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                             QHBoxLayout, QMessageBox)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QSize
import sqlite3
from utils.launcher_tools import safe_launch
from admin.views.dialogs.app import AppEditor  # Для редактирования приложений


class ChatMenu(QWidget):
    def __init__(self, switch_to, is_admin=False):
        super().__init__()
        self.switch_to = switch_to
        self.is_admin = is_admin  # Флаг администратора
        self.init_ui()
        self.load_chats_from_db()  # Загрузка чатов из БД

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(50, 50, 50, 50)

        # Стили для элементов
        self.title_style = """
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
        """

        self.chat_button_style = """
            QPushButton {
                background-color: rgba(100, 180, 100, 0.85);
                color: white;
                font-size: 18px;
                padding: 15px;
                border-radius: 8px;
                border: 2px solid #64B464;
                min-width: 300px;
            }
            QPushButton:hover {
                background-color: rgba(120, 200, 120, 0.9);
            }
        """

        self.admin_button_style = """
            QPushButton {
                background-color: rgba(180, 180, 50, 0.85);
                color: white;
                font-size: 14px;
                padding: 5px;
                border-radius: 5px;
                border: 1px solid #B4B432;
                min-width: 30px;
                max-width: 30px;
            }
            QPushButton:hover {
                background-color: rgba(200, 200, 70, 0.9);
            }
        """

        self.back_button_style = """
            QPushButton {
                background-color: rgba(200, 80, 80, 0.85);
                color: white;
                font-size: 18px;
                padding: 15px;
                border-radius: 8px;
                border: 2px solid #C85050;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: rgba(220, 100, 100, 0.9);
            }
        """

        # Заголовок
        title = QLabel("Общение")
        title.setStyleSheet(self.title_style)
        self.layout.addWidget(title)

        # Контейнер для списка чатов
        self.chats_container = QWidget()
        self.chats_layout = QVBoxLayout()
        self.chats_container.setLayout(self.chats_layout)
        self.layout.addWidget(self.chats_container)

        # Кнопка "Назад"
        back_btn = QPushButton("Назад")
        back_btn.setStyleSheet(self.back_button_style)
        back_btn.clicked.connect(lambda: self.switch_to("main"))
        self.layout.addWidget(back_btn)

        # Кнопка "Добавить чат" (только для админа)
        if self.is_admin:
            add_btn = QPushButton("Добавить мессенджер")
            add_btn.setStyleSheet(self.chat_button_style)
            add_btn.clicked.connect(self.add_chat)
            self.layout.addWidget(add_btn)

        self.setLayout(self.layout)

    def load_chats_from_db(self):
        """Загрузка чатов из базы данных"""
        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()

        # Получаем чаты из категории "Общение" (category_id=2)
        c.execute("""SELECT id, name, path, icon_path FROM apps 
                     WHERE category_id=2 ORDER BY name""")
        chats = c.fetchall()
        conn.close()

        # Очищаем текущий список
        for i in reversed(range(self.chats_layout.count())):
            self.chats_layout.itemAt(i).widget().setParent(None)

        # Добавляем чаты
        for chat_id, name, path, icon_path in chats:
            self.add_chat_button(chat_id, name, path, icon_path)

    def add_chat_button(self, chat_id, name, path, icon_path=None):
        """Добавляет кнопку чата в интерфейс"""
        btn_layout = QHBoxLayout()

        # Основная кнопка чата
        chat_btn = QPushButton(name)
        chat_btn.setStyleSheet(self.chat_button_style)

        if icon_path and os.path.exists(icon_path):
            chat_btn.setIcon(QIcon(icon_path))
            chat_btn.setIconSize(QSize(32, 32))

        chat_btn.clicked.connect(lambda _, p=path: safe_launch(p, self))
        btn_layout.addWidget(chat_btn)

        # Кнопки редактирования (только для админа)
        if self.is_admin:
            edit_btn = QPushButton("✏")
            edit_btn.setStyleSheet(self.admin_button_style)
            edit_btn.clicked.connect(lambda _, cid=chat_id: self.edit_chat(cid))
            btn_layout.addWidget(edit_btn)

            delete_btn = QPushButton("✖")
            delete_btn.setStyleSheet(self.admin_button_style)
            delete_btn.clicked.connect(lambda _, cid=chat_id: self.delete_chat(cid))
            btn_layout.addWidget(delete_btn)

        self.chats_layout.addLayout(btn_layout)

    def add_chat(self):
        """Добавление нового чата"""
        dialog = AppEditor(category_id=2, parent=self)  # category_id=2 для чатов
        if dialog.exec():
            self.load_chats_from_db()

    def edit_chat(self, chat_id):
        """Редактирование существующего чата"""
        dialog = AppEditor(app_id=chat_id, parent=self)
        if dialog.exec():
            self.load_chats_from_db()

    def delete_chat(self, chat_id):
        """Удаление чата"""
        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить этот мессенджер?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('launcher.db')
            c = conn.cursor()
            c.execute("DELETE FROM apps WHERE id=?", (chat_id,))
            conn.commit()
            conn.close()
            self.load_chats_from_db()