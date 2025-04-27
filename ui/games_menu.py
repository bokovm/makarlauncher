from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                             QMessageBox, QHBoxLayout, QSizePolicy)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
import os
import subprocess
from utils.json_utils import load_json, save_json

class GamesMenu(QWidget):
    def __init__(self, switch_to, is_admin=False):
        super().__init__()
        self.switch_to = switch_to
        self.is_admin = is_admin
        self.games_file = "data/games.json"  # Путь к JSON файлу с играми
        self.init_ui()
        self.load_games()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setStyleSheet("background-color: #2b2b2b;")
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(30, 30, 30, 30)

        # Заголовок
        title = QLabel("Игры")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
        """)
        self.layout.addWidget(title)

        # Контейнер для списка игр
        self.games_container = QWidget()
        self.games_container.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.games_layout = QVBoxLayout()
        self.games_layout.setSpacing(15)
        self.games_container.setLayout(self.games_layout)
        self.layout.addWidget(self.games_container)

        # Кнопка "Назад"
        back_btn = QPushButton("Назад")
        back_btn.setStyleSheet("""
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
        """)
        back_btn.clicked.connect(lambda: self.switch_to("main"))
        self.layout.addWidget(back_btn)

        # Кнопка "Добавить игру" (для админа)
        if self.is_admin:
            add_btn = QPushButton("Добавить игру")
            add_btn.setStyleSheet("""
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
            """)
            add_btn.clicked.connect(self.add_game)
            self.layout.addWidget(add_btn)

        self.setLayout(self.layout)

    def load_games(self):
        """Загрузка списка игр из JSON файла"""
        self.clear_games_layout()
        games = load_json(self.games_file)

        if not games:
            self.show_no_games_message()
            return

        for game in games:
            self.add_game_button(game)

    def clear_games_layout(self):
        """Очистка layout с играми"""
        while self.games_layout.count():
            item = self.games_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def show_no_games_message(self):
        """Показать сообщение об отсутствии игр"""
        label = QLabel("Игры не найдены")
        label.setStyleSheet("color: white; font-size: 16px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.games_layout.addWidget(label)

    def add_game_button(self, game):
        """Добавление кнопки игры в интерфейс"""
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        # Кнопка игры
        game_btn = QPushButton(game['name'])
        game_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(75, 150, 200, 0.85);
                color: white;
                font-size: 18px;
                padding: 15px;
                border-radius: 8px;
                border: 2px solid #4B96C8;
                min-width: 300px;
                text-align: left;
            }
            QPushButton:hover {
                background-color: rgba(95, 170, 220, 0.9);
            }
        """)
        game_btn.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )

        # Установка иконки если она существует
        if game.get("icon_path") and os.path.exists(game["icon_path"]):
            game_btn.setIcon(QIcon(game["icon_path"]))
            game_btn.setIconSize(QSize(32, 32))

        game_btn.clicked.connect(lambda _, p=game["path"]: self.launch_game(p))
        btn_layout.addWidget(game_btn)

        # Кнопки управления для админа
        if self.is_admin:
            self.add_admin_buttons(btn_layout, game)

        self.games_layout.addLayout(btn_layout)

    def add_admin_buttons(self, layout, game):
        """Добавление кнопок управления для администратора"""
        # Кнопка редактирования
        edit_btn = QPushButton("✏")
        edit_btn.setToolTip("Редактировать игру")
        edit_btn.clicked.connect(lambda: self.edit_game(game))
        layout.addWidget(edit_btn)

        # Кнопка удаления
        delete_btn = QPushButton("🗑")
        delete_btn.setToolTip("Удалить игру")
        delete_btn.clicked.connect(lambda: self.delete_game(game))
        layout.addWidget(delete_btn)

    def launch_game(self, path):
        """Запуск игры"""
        if not os.path.exists(path):
            QMessageBox.critical(self, "Ошибка запуска", f"Файл игры не найден: {path}")
            return

        try:
            if os.name == "nt":
                subprocess.Popen(path, shell=True)
            else:
                subprocess.Popen([path])
        except Exception as e:
            QMessageBox.critical(self, "Ошибка запуска", f"Не удалось запустить игру: {e}")

    def add_game(self):
        """Добавление новой игры"""
        games = load_json(self.games_file)
        new_game = {
            "id": len(games) + 1,
            "name": "Новая игра",
            "path": "",
            "icon_path": ""
        }
        games.append(new_game)
        save_json(self.games_file, games)
        self.load_games()

    def edit_game(self, game):
        """Редактирование игры (заглушка)"""
        print(f"Редактирование игры: {game}")

    def delete_game(self, game):
        """Удаление игры"""
        confirm = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Вы уверены, что хотите удалить игру: {game['name']}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            games = load_json(self.games_file)
            games = [g for g in games if g["id"] != game["id"]]
            save_json(self.games_file, games)
            self.load_games()