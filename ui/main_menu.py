from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
import os
from utils.json_utils import load_json


class MainMenu(QWidget):
    def __init__(self, switch_callback, admin_auth_callback):
        """
        Конструктор для главного меню
        :param switch_callback: Функция для переключения экранов
        :param admin_auth_callback: Функция для вызова авторизации администратора
        """
        super().__init__()
        self.switch_callback = switch_callback
        self.admin_auth_callback = admin_auth_callback
        self.init_ui()

    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.update_layout()

    def update_layout(self):
        """Обновление интерфейса с категориями и приложениями"""
        # Очищаем текущий layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Загружаем категории и приложения
        categories = load_json("data/categories.json")
        apps = load_json("data/apps.json")

        for category in categories:
            # Добавляем заголовок категории
            category_label = QLabel(category["name"])
            category_label.setStyleSheet("font-size: 20px; color: white; margin-top: 20px;")
            self.layout.addWidget(category_label)

            # Контейнер для приложений в данной категории
            apps_container = QWidget()
            apps_layout = QHBoxLayout()
            apps_container.setLayout(apps_layout)

            for app in filter(lambda x: x["category_id"] == category["id"], apps):
                app_btn = QPushButton(app["name"])
                app_btn.setStyleSheet("""
                    QPushButton {
                        font-size: 16px;
                        background-color: #4682B4;
                        color: white;
                        padding: 10px;
                        border-radius: 5px;
                        border: none;
                    }
                    QPushButton:hover {
                        background-color: #5A9BD5;
                    }
                """)
                app_btn.clicked.connect(lambda _, p=app["path"]: self.launch_app(p))
                apps_layout.addWidget(app_btn)

            self.layout.addWidget(apps_container)

        # Кнопка для входа в админ-панель
        admin_btn = QPushButton("Админ-панель")
        admin_btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        admin_btn.clicked.connect(self.admin_auth_callback)
        self.layout.addWidget(admin_btn)

    def launch_app(self, path):
        """Запуск приложения"""
        if os.path.exists(path):
            os.startfile(path)
        else:
            print(f"[ERROR] Приложение не найдено по пути: {path}")