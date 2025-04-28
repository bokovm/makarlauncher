import logging
import sys
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QStackedWidget, QPushButton,
                             QHBoxLayout, QMessageBox, QDialog)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QPalette, QBrush, QColor, QIcon

from ui.main_menu import MainMenu
from ui.browser_menu import BrowserMenu
from ui.games_menu import GamesMenu
from ui.chat_menu import ChatMenu
from ui.settings_menu import SettingsMenu
from admin.auth import AdminLoginDialog
from admin.views.panels import AdminPanel


class Launcher(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()

        # Настройка логирования
        self.setup_logging()

        # Основные настройки окна
        self.is_fullscreen = False
        self.setWindowTitle("Лаунчер для бабушки")
        self.setMinimumSize(800, 600)

        # Инициализация атрибутов
        self.stack = stacked_widget
        self.admin_panel = None  # Будет инициализировано при первом входе
        self.admin_button = QPushButton()
        self.toggle_button = QPushButton()
        self.menus = {}

        # Настройка фона и интерфейса
        self.setup_background()
        self.setup_ui()

    def setup_logging(self):
        """Настройка системы логирования"""
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("launcher.log"),
                logging.StreamHandler()
            ]
        )

    def setup_background(self):
        """Настройка фонового изображения"""
        bg_path = self.resource_path('assets/background.jpg')
        palette = self.palette()

        if os.path.exists(bg_path):
            pixmap = QPixmap(bg_path)
            if not pixmap.isNull():
                palette.setBrush(QPalette.ColorRole.Window,
                                 QBrush(pixmap.scaled(
                                     self.size(),
                                     Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                     Qt.TransformationMode.SmoothTransformation)))
            else:
                logging.warning(f"Не удалось загрузить фоновое изображение: {bg_path}")
                palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
        else:
            logging.warning(f"Фоновое изображение не найдено: {bg_path}")
            palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))

        self.setPalette(palette)

    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Стилизация стека
        self.stack.setStyleSheet("""
            QStackedWidget {
                background: transparent;
                border: none;
            }
        """)

        # Инициализация пользовательских меню
        try:
            self.menus = {
                "main": MainMenu(self.switch_to, self.show_admin_auth),
                "games": GamesMenu(self.switch_to),
                "browser": BrowserMenu(self.switch_to),
                "chat": ChatMenu(self.switch_to),
                "settings": SettingsMenu(self.switch_to),
            }

            # Добавление меню в стек
            for name, menu in self.menus.items():
                menu.setStyleSheet("background: transparent;")
                self.stack.addWidget(menu)
                logging.debug(f"Меню '{name}' успешно добавлено")
        except Exception as e:
            logging.error(f"Ошибка при инициализации меню: {e}")
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить интерфейс")

        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Панель верхних кнопок
        top_button_layout = QHBoxLayout()
        top_button_layout.setContentsMargins(0, 0, 0, 0)
        top_button_layout.setSpacing(10)
        top_button_layout.setAlignment(Qt.AlignmentFlag.AlignRight)

        # Настройка кнопки администратора
        self.setup_admin_button(top_button_layout)

        # Настройка кнопки переключения режима
        self.setup_toggle_button(top_button_layout)

        # Добавляем все в основной layout
        main_layout.addLayout(top_button_layout)
        main_layout.addWidget(self.stack, stretch=1)
        self.setLayout(main_layout)

        # Стартовый экран
        self.switch_to("main")
        self.showFullScreen()

    def setup_admin_button(self, layout):
        """Настройка кнопки администратора"""
        admin_icon = self.load_icon("assets/admin_icon.png")
        self.admin_button.setIcon(admin_icon)
        self.admin_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                padding: 8px;
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.4);
            }
        """)
        self.admin_button.setIconSize(QSize(30, 30))
        self.admin_button.setToolTip("Админ-панель")
        self.admin_button.clicked.connect(self.show_admin_auth)
        layout.addWidget(self.admin_button)

    def setup_toggle_button(self, layout):
        """Настройка кнопки переключения режима"""
        fullscreen_icon = self.load_icon("assets/fullscreen_icon.png")
        self.toggle_button.setIcon(fullscreen_icon)
        self.toggle_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                padding: 8px;
                border: 1px solid rgba(255, 255, 255, 0.4);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.4);
            }
        """)
        self.toggle_button.setIconSize(QSize(30, 30))
        self.toggle_button.setToolTip("Полноэкранный режим")
        self.toggle_button.clicked.connect(self.toggle_fullscreen)
        layout.addWidget(self.toggle_button)

    def load_icon(self, path):
        """Загрузка иконки с обработкой ошибок"""
        icon_path = self.resource_path(path)
        if os.path.exists(icon_path):
            return QIcon(icon_path)
        logging.warning(f"Иконка не найдена: {icon_path}")
        return QIcon()

    def show_admin_auth(self):
        """
        Показывает диалог авторизации администратора
        """
        try:
            # Вызываем авторизацию только здесь
            dialog = AdminLoginDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                if self.admin_panel is None:
                    self.admin_panel = AdminPanel(self)
                    self.stack.addWidget(self.admin_panel)
                    logging.debug("Админ-панель инициализирована")

                self.stack.setCurrentWidget(self.admin_panel)
                self.admin_button.hide()
                logging.info("Успешный вход в админ-панель")
            else:
                logging.warning("Неудачная попытка входа в админ-панель")
                QMessageBox.warning(self, "Ошибка", "Неверный пароль администратора")
        except Exception as e:
            logging.error(f"Ошибка при загрузке админ-панели: {e}", exc_info=True)
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить админ-панель:\n{str(e)}")

    def switch_to(self, screen_name):
        """Переключение между экранами"""
        try:
            if screen_name not in self.menus:
                logging.error(f"Попытка переключения на несуществующий экран: {screen_name}")
                return

            self.stack.setCurrentWidget(self.menus[screen_name])
            self.admin_button.setVisible(screen_name == "main")
            logging.debug(f"Переключено на экран: {screen_name}")
        except Exception as e:
            logging.error(f"Ошибка при переключении экрана: {e}", exc_info=True)
            QMessageBox.critical(self, "Ошибка", "Не удалось переключить экран")

    def toggle_fullscreen(self):
        """Переключение между полноэкранным и оконным режимом"""
        try:
            if self.isFullScreen():
                self.showNormal()
                icon_path = "assets/windowed_icon.png"
                self.toggle_button.setToolTip("Переключить в полноэкранный режим")
            else:
                self.showFullScreen()
                icon_path = "assets/fullscreen_icon.png"
                self.toggle_button.setToolTip("Переключить в оконный режим")

            icon = self.load_icon(icon_path)
            self.toggle_button.setIcon(icon)
            logging.debug(f"Режим переключен: {'Полноэкранный' if self.isFullScreen() else 'Оконный'}")
        except Exception as e:
            logging.error(f"Ошибка при переключении режима: {e}", exc_info=True)

    def resizeEvent(self, event):
        """Обработка изменения размера окна"""
        try:
            palette = self.palette()
            brush = palette.brush(QPalette.ColorRole.Window)
            if not brush.texture().isNull():
                pixmap = brush.texture()
                palette.setBrush(QPalette.ColorRole.Window,
                                 QBrush(pixmap.scaled(
                                     self.size(),
                                     Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                                     Qt.TransformationMode.SmoothTransformation)))
                self.setPalette(palette)
            super().resizeEvent(event)
        except Exception as e:
            logging.error(f"Ошибка при обработке изменения размера: {e}")

    @staticmethod
    def resource_path(relative_path):
        """Возвращает правильный путь для ресурсов"""
        try:
            if getattr(sys, 'frozen', False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.abspath(".")

            full_path = os.path.join(base_path, relative_path)
            logging.debug(f"Ресурсный путь: {relative_path} -> {full_path}")
            return full_path
        except Exception as e:
            logging.error(f"Ошибка при получении ресурсного пути: {relative_path} - {e}")
            return relative_path