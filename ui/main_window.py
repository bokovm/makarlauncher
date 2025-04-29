from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QDialog, QToolBar
import json
import os
from admin.auth import AdminLoginDialog
from ui.main_menu import MainMenu
from admin.views.panels import AdminPanel
from utils.helpers import resource_path
import logging


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лаунчер")
        self.setMinimumSize(800, 600)

        # Инициализация JSON файла настроек
        self.settings_file = "data/settings.json"
        self._init_settings_file()

        # Создаем виджет с переключением между экранами
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Флаг полноэкранного режима
        self.is_fullscreen = False

        # Инициализация экранов
        self.main_menu = MainMenu(self.switch_to_screen, self.show_admin_panel)
        self.admin_panel = AdminPanel(self)

        # Добавляем экраны в стек
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.admin_panel)

        # Инициализируем панель инструментов
        self.init_toolbar()

        # Загрузка настроек и отображение главного меню
        self.load_settings()
        self.show_main_menu()

    def _init_settings_file(self):
        """Инициализация файла настроек, если он не существует"""
        if not os.path.exists(self.settings_file):
            default_settings = {
                "background_image": "",
                "background_color": "#ffffff",
                "opacity": 1.0,
                "font_family": "Arial"
            }
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            with open(self.settings_file, 'w') as f:
                json.dump(default_settings, f, indent=4)

    def init_toolbar(self):
        """Инициализация панели инструментов"""
        toolbar = QToolBar("Основная панель")
        toolbar.setIconSize(Qt.QSize(24, 24))
        self.addToolBar(toolbar)

        # Кнопка переключения полноэкранного режима
        fullscreen_action = QAction(QIcon(resource_path("assets/fullscreen_icon.png")),
                                 "Полноэкранный режим", self)
        fullscreen_action.triggered.connect(self.toggle_fullscreen)
        toolbar.addAction(fullscreen_action)

        # Кнопка выхода
        exit_action = QAction(QIcon(resource_path("assets/exit_icon.png")), "Выход", self)
        exit_action.triggered.connect(self.close)
        toolbar.addAction(exit_action)

    def toggle_fullscreen(self):
        """Переключение между полноэкранным и оконным режимом"""
        if self.isFullScreen():
            self.showNormal()
            self.is_fullscreen = False
        else:
            self.showFullScreen()
            self.is_fullscreen = True

    def switch_to_screen(self, screen_name):
        """Переключение между экранами"""
        if screen_name == "main":
            self.stacked_widget.setCurrentWidget(self.main_menu)
        elif screen_name == "admin":
            self.stacked_widget.setCurrentWidget(self.admin_panel)

    def show_main_menu(self):
        """Отображение главного меню"""
        if self.main_menu:
            self.stacked_widget.setCurrentWidget(self.main_menu)
        else:
            logging.error("Главное меню не инициализировано")

    def show_admin_panel(self):
        """Отображение панели администратора с авторизацией"""
        dialog = AdminLoginDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.stacked_widget.setCurrentWidget(self.admin_panel)

    def load_settings(self):
        """Загрузка настроек из JSON файла и применение их"""
        try:
            with open(self.settings_file, 'r') as f:
                settings = json.load(f)

            # Формируем стиль в зависимости от данных из настроек
            style = []
            if settings.get("background_image"):
                bg_image = settings["background_image"]
                style.append(f"background-image: url({bg_image});")
                style.append("background-repeat: no-repeat;")
                style.append("background-position: center;")
                style.append("background-size: cover;")

            if settings.get("background_color"):
                style.append(f"background-color: {settings['background_color']};")

            if settings.get("opacity"):
                style.append(f"opacity: {settings['opacity']};")

            if settings.get("font_family"):
                style.append(f"font-family: '{settings['font_family']}';")

            # Применяем стиль к главному окну
            self.setStyleSheet("QWidget { " + " ".join(style) + " }")

        except Exception as e:
            logging.error(f"Ошибка при загрузке настроек: {e}")

    def apply_settings(self):
        """Применение настроек и обновление интерфейса"""
        self.load_settings()
        if self.main_menu:
            self.main_menu.update_layout()