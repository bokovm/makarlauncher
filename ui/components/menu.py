from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QHBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon
import sqlite3
import os
import webbrowser


class MainMenu(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)
        self.update_layout()

    def update_layout(self):
        """Обновление интерфейса с категориями и приложениями."""
        # Очищаем текущий layout
        self.clear_layout(self.layout)

        # Загружаем категории и приложения
        try:
            categories = load_json("data/categories.json") or []
            apps = load_json("data/apps.json") or []
        except Exception as e:
            self.show_message(f"Ошибка загрузки данных: {str(e)}")
            return

        if not categories:
            self.show_message("Категории не найдены в JSON-файле.")
            return

        for category in categories:
            # Добавляем заголовок категории
            category_label = QLabel(category.get("name", "Без имени"))
            category_label.setStyleSheet("font-size: 20px; color: white; margin-top: 20px;")
            self.layout.addWidget(category_label)

            # Фильтруем приложения по категории
            category_apps = [app for app in apps if app.get("category_id") == category.get("id")]

            if not category_apps:
                empty_label = QLabel("(Нет приложений в категории)")
                empty_label.setStyleSheet("font-size: 14px; color: gray;")
                self.layout.addWidget(empty_label)
                continue

            # Создаем контейнер для приложений
            apps_container = QWidget()
            apps_layout = QHBoxLayout()
            apps_layout.setSpacing(10)
            apps_layout.setContentsMargins(0, 10, 0, 10)  # Отступы для кнопок
            apps_container.setLayout(apps_layout)

            for app in category_apps:
                app_btn = self.create_app_button(app)
                apps_layout.addWidget(app_btn)

            self.layout.addWidget(apps_container)

            # Добавляем разделитель между категориями
            spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
            self.layout.addItem(spacer)

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
        self.layout.addWidget(admin_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def create_app_button(self, app):
        """
        Создает кнопку для приложения.
        :param app: Словарь с данными приложения (name, path, icon_path, bg_color, is_square).
        :return: QPushButton
        """
        app_name = app.get("name", "Без имени")
        app_path = app.get("path", "")
        bg_color = app.get("bg_color", "#4682B4")
        is_square = app.get("is_square", False)

        app_btn = QPushButton(app_name)
        app_btn.setToolTip(app_name)

        # Изменяем размер кнопки для адаптации
        if is_square:
            app_btn.setMinimumSize(80, 80)  # Минимальный размер кнопки
            app_btn.setMaximumSize(150, 150)  # Максимальный размер кнопки
        else:
            app_btn.setMinimumHeight(64)  # Минимальная высота для не квадратных кнопок

        app_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        app_btn.setStyleSheet(f"""
            QPushButton {{
                font-size: 16px;
                background-color: {bg_color};
                color: white;
                padding: 10px;
                border-radius: {'10px' if is_square else '32px'};
                border: none;
            }}
            QPushButton:hover {{
                background-color: #5A9BD5;
            }}
        """)

        app_btn.clicked.connect(lambda _, p=app_path: self.launch_app(p))
        return app_btn

    def launch_app(self, path):
        """Запуск приложения"""
        try:
            if os.path.exists(path):
                os.startfile(path)
            else:
                QMessageBox.critical(self, "Ошибка", f"Приложение не найдено по пути: {path}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить приложение:\n{e}")

    def show_message(self, message):
        """Отображение сообщения"""
        QMessageBox.information(self, "Информация", message)