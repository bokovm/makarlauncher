from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                             QMessageBox, QHBoxLayout)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt, QSize
import subprocess
import os
import sqlite3
from admin.views.dialogs.app import AppEditor  # Для редактирования игр


class GamesMenu(QWidget):
    def __init__(self, switch_to, is_admin=False):
        super().__init__()
        self.switch_to = switch_to
        self.is_admin = is_admin  # Флаг администратора
        self.init_ui()
        self.load_games_from_db()  # Загрузка игр из БД

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

        self.game_button_style = """
            QPushButton {
                background-color: rgba(75, 150, 200, 0.85);
                color: white;
                font-size: 18px;
                padding: 15px;
                border-radius: 8px;
                border: 2px solid #4B96C8;
                min-width: 300px;
            }
            QPushButton:hover {
                background-color: rgba(95, 170, 220, 0.9);
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
        title = QLabel("Игры")
        title.setStyleSheet(self.title_style)
        self.layout.addWidget(title)

        # Контейнер для списка игр
        self.games_container = QWidget()
        self.games_layout = QVBoxLayout()
        self.games_container.setLayout(self.games_layout)
        self.layout.addWidget(self.games_container)

        # Кнопка "Назад"
        back_btn = QPushButton("Назад")
        back_btn.setStyleSheet(self.back_button_style)
        back_btn.clicked.connect(lambda: self.switch_to("main"))
        self.layout.addWidget(back_btn)

        # Кнопка "Добавить игру" (только для админа)
        if self.is_admin:
            add_btn = QPushButton("Добавить игру")
            add_btn.setStyleSheet(self.game_button_style)
            add_btn.clicked.connect(self.add_game)
            self.layout.addWidget(add_btn)

        self.setLayout(self.layout)

    def load_games_from_db(self):
        """Загрузка игр из базы данных"""
        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()

        # Получаем игры из категории "Игры" (category_id=1)
        c.execute("""SELECT id, name, path, icon_path FROM apps 
                     WHERE category_id=1 ORDER BY name""")
        games = c.fetchall()
        conn.close()

        # Очищаем текущий список
        for i in reversed(range(self.games_layout.count())):
            self.games_layout.itemAt(i).widget().setParent(None)

        # Добавляем игры
        for game_id, name, path, icon_path in games:
            self.add_game_button(game_id, name, path, icon_path)

    def add_game_button(self, game_id, name, path, icon_path=None):
        """Добавляет кнопку игры в интерфейс"""
        btn_layout = QHBoxLayout()

        # Основная кнопка игры
        game_btn = QPushButton(name)
        game_btn.setStyleSheet(self.game_button_style)

        if icon_path and os.path.exists(icon_path):
            game_btn.setIcon(QIcon(icon_path))
            game_btn.setIconSize(QSize(32, 32))

        game_btn.clicked.connect(lambda _, p=path, n=name: self.launch_game(p, n))
        btn_layout.addWidget(game_btn)

        # Кнопки редактирования (только для админа)
        if self.is_admin:
            edit_btn = QPushButton("✏")
            edit_btn.setStyleSheet(self.admin_button_style)
            edit_btn.clicked.connect(lambda _, gid=game_id: self.edit_game(gid))
            btn_layout.addWidget(edit_btn)

            delete_btn = QPushButton("✖")
            delete_btn.setStyleSheet(self.admin_button_style)
            delete_btn.clicked.connect(lambda _, gid=game_id: self.delete_game(gid))
            btn_layout.addWidget(delete_btn)

        self.games_layout.addLayout(btn_layout)

    def launch_game(self, path, name):
        """Запуск игры с обработкой ошибок"""
        if os.path.exists(path):
            try:
                # Запуск игры без консоли (для Windows)
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                subprocess.Popen(
                    path,
                    startupinfo=startupinfo,
                    shell=True
                )
            except Exception as e:
                self.show_error_message(
                    "Ошибка запуска",
                    f"Не удалось запустить {name}.\n\nОшибка: {str(e)}"
                )
        else:
            self.show_error_message(
                "Файл не найден",
                f"Путь к игре {name} не найден:\n{path}"
            )

    def add_game(self):
        """Добавление новой игры"""
        dialog = AppEditor(category_id=1, parent=self)  # category_id=1 для игр
        if dialog.exec():
            self.load_games_from_db()

    def edit_game(self, game_id):
        """Редактирование существующей игры"""
        dialog = AppEditor(app_id=game_id, parent=self)
        if dialog.exec():
            self.load_games_from_db()

    def delete_game(self, game_id):
        """Удаление игры"""
        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить эту игру?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('launcher.db')
            c = conn.cursor()
            c.execute("DELETE FROM apps WHERE id=?", (game_id,))
            conn.commit()
            conn.close()
            self.load_games_from_db()

    def show_error_message(self, title, message):
        """Показать сообщение об ошибке"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #333333;
            }
            QLabel {
                color: white;
            }
            QPushButton {
                min-width: 80px;
                padding: 5px;
            }
        """)
        msg.exec()