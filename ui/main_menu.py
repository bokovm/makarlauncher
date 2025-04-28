from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QMessageBox, QSizePolicy
from PyQt6.QtCore import Qt
import os
from utils.json_utils import load_json


class MainMenu(QWidget):
    def __init__(self, switch_callback, admin_auth_callback):
        """
        Конструктор для главного меню.
        :param switch_callback: Функция для переключения экранов.
        :param admin_auth_callback: Функция для вызова авторизации администратора.
        """
        super().__init__()
        self.switch_callback = switch_callback
        self.admin_auth_callback = admin_auth_callback
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.current_category = None  # Для отслеживания текущей категории
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса."""
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.show_categories()

    def show_categories(self):
        """Отображение списка категорий."""
        self.clear_layout(self.layout)

        try:
            categories = load_json("data/categories.json") or []
        except Exception as e:
            self.show_message(f"Ошибка загрузки данных категорий: {str(e)}")
            return

        if not categories:
            self.show_message("Категории не найдены в JSON-файле.")
            return

        # Заголовок
        title_label = QLabel("Выберите категорию:")
        title_label.setStyleSheet("font-size: 20px; color: white;")
        self.layout.addWidget(title_label)

        # Создание кнопок категорий
        for category in categories:
            category_button = QPushButton(category.get("name", "Без имени"))
            category_button.setStyleSheet("""
                QPushButton {
                    font-size: 16px;
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px;
                    border-radius: 5px;
                    border: none;
                    margin-bottom: 10px;
                }
                QPushButton:hover {
                    background-color: #45A049;
                }
            """)
            category_button.clicked.connect(lambda _, c=category: self.show_apps(c))
            self.layout.addWidget(category_button)

    def show_apps(self, category):
        """Отображение приложений из выбранной категории."""
        self.clear_layout(self.layout)

        # Заголовок категории
        category_label = QLabel(f"Категория: {category.get('name', 'Без имени')}")
        category_label.setStyleSheet("font-size: 20px; color: white;")
        self.layout.addWidget(category_label)

        try:
            apps = load_json("data/apps.json") or []
        except Exception as e:
            self.show_message(f"Ошибка загрузки данных приложений: {str(e)}")
            return

        # Фильтруем приложения по категории
        category_apps = [app for app in apps if app.get("category_id") == category.get("id")]

        if not category_apps:
            empty_label = QLabel("(Нет приложений в категории)")
            empty_label.setStyleSheet("font-size: 14px; color: gray;")
            self.layout.addWidget(empty_label)
        else:
            # Создаём кнопки для приложений
            apps_container = QWidget()
            apps_layout = QHBoxLayout()
            apps_layout.setSpacing(10)
            apps_container.setLayout(apps_layout)

            for app in category_apps:
                app_btn = self.create_app_button(app)
                apps_layout.addWidget(app_btn)

            self.layout.addWidget(apps_container)

        # Кнопка "Назад"
        back_button = QPushButton("Назад")
        back_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                border: none;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #45A049;
            }
        """)
        back_button.clicked.connect(self.show_categories)
        self.layout.addWidget(back_button)

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

        # Настройки размеров
        app_btn.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        if is_square:
            app_btn.setFixedSize(100, 100)

        app_btn.setStyleSheet(f"""
            QPushButton {{
                font-size: 14px;
                background-color: {bg_color};
                color: white;
                padding: 5px;
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
        """
        Запуск приложения.
        :param path: Путь к приложению.
        """
        if not path:
            self.show_message("Путь к приложению не указан")
            return

        if os.path.exists(path):
            try:
                if os.name == 'nt':  # Windows
                    os.startfile(path)
                elif os.name == 'posix':  # Linux, Mac
                    os.system(f'xdg-open "{path}"')
            except Exception as e:
                self.show_message(f"Не удалось запустить приложение: {str(e)}")
        else:
            self.show_message(f"Приложение не найдено по пути: {path}")

    def clear_layout(self, layout):
        """Очищает layout от всех виджетов."""
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_message(self, message):
        """
        Отображение сообщения пользователю.
        :param message: Текст сообщения.
        """
        QMessageBox.critical(self, "Ошибка", message)