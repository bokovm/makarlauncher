import sys
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QStackedWidget, QApplication,
                             QPushButton, QHBoxLayout, QMessageBox, QDialog)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import (QPixmap, QPalette, QBrush, QColor, QIcon, QFont)

from ui.main_menu import MainMenu
from ui.browser_menu import BrowserMenu
from ui.games_menu import GamesMenu
from ui.chat_menu import ChatMenu
from ui.settings_menu import SettingsMenu
from admin.auth import AdminLoginDialog  # Импорт админ-авторизации
from admin.views.panels import AdminPanel  # Импорт админ-панели


def resource_path(relative_path):
    """Возвращает правильный путь для ресурсов"""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class Launcher(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setWindowTitle("Лаунчер для бабушки")
        self.setMinimumSize(800, 600)
        self.setup_background()
        self.setup_ui(stacked_widget)
        self.admin_panel = None  # Будет инициализировано при первом входе

    def setup_background(self):
        """Настройка фонового изображения"""
        bg_path = resource_path('assets/background.jpg')
        pixmap = QPixmap(bg_path)

        if pixmap.isNull():
            palette = self.palette()
            palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
            self.setPalette(palette)
        else:
            palette = self.palette()
            palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap.scaled(
                self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)))
            self.setPalette(palette)

    def setup_ui(self, stacked_widget):
        """Настройка пользовательского интерфейса"""
        self.stack = stacked_widget
        self.stack.setStyleSheet("background: transparent;")

        # Инициализация пользовательских меню
        self.menus = {
            "main": MainMenu(self.switch_to, self.show_admin_auth),
            "games": GamesMenu(self.switch_to),
            "browser": BrowserMenu(self.switch_to),
            "chat": ChatMenu(self.switch_to),
            "settings": SettingsMenu(self.switch_to),
        }

        # Добавление меню в стек
        for menu in self.menus.values():
            menu.setStyleSheet("background: transparent;")
            self.stack.addWidget(menu)

        # Основной layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Панель верхних кнопок
        top_button_layout = QHBoxLayout()
        top_button_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        # Кнопка админ-панели (только в основном меню)
        self.admin_button = QPushButton()
        self.admin_button.setIcon(QIcon(resource_path("assets/admin_icon.png")))
        self.admin_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 15px;
                padding: 8px;
                border: 1px solid rgba(255, 255, 255, 0.4);
                margin-right: 10px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.3);
            }
        """)
        self.admin_button.setIconSize(QSize(30, 30))
        self.admin_button.clicked.connect(self.show_admin_auth)
        top_button_layout.addWidget(self.admin_button)

        # Кнопка переключения режима
        self.toggle_button = QPushButton()
        self.toggle_button.setIcon(QIcon(resource_path("assets/fullscreen_icon.png")))
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
        """)
        self.toggle_button.setIconSize(QSize(30, 30))
        self.toggle_button.clicked.connect(self.toggle_fullscreen)
        top_button_layout.addWidget(self.toggle_button)

        # Добавляем все в основной layout
        main_layout.addLayout(top_button_layout)
        main_layout.addWidget(self.stack)
        self.setLayout(main_layout)

        # Стартовый экран
        self.switch_to("main")
        self.showFullScreen()

    def show_admin_auth(self):
        """Показывает диалог авторизации администратора"""
        if not self.admin_panel:
            # Инициализируем админ-панель при первом входе
            self.admin_panel = AdminPanel(self)
            self.admin_panel.setStyleSheet("background: transparent;")
            self.stack.addWidget(self.admin_panel)

        dialog = AdminLoginDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.stack.setCurrentWidget(self.admin_panel)
            self.admin_button.hide()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный пароль администратора")

    def switch_to(self, screen_name):
        """Переключение между экранами"""
        if screen_name == "main":
            self.admin_button.show()
        else:
            self.admin_button.hide()

        if screen_name in self.menus:
            self.stack.setCurrentWidget(self.menus[screen_name])

    def toggle_fullscreen(self):
        """Переключение между полноэкранным и оконным режимом"""
        if self.isFullScreen():
            self.showNormal()
            self.toggle_button.setIcon(QIcon(resource_path("assets/fullscreen_icon.png")))
        else:
            self.showFullScreen()
            self.toggle_button.setIcon(QIcon(resource_path("assets/windowed_icon.png")))

    def resizeEvent(self, event):
        """Обработка изменения размера окна"""
        # Масштабирование фона
        palette = self.palette()
        if not palette.brush(QPalette.ColorRole.Window).texture().isNull():
            pixmap = palette.brush(QPalette.ColorRole.Window).texture()
            palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap.scaled(
                self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)))
            self.setPalette(palette)

        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    launcher = Launcher(stacked_widget)
    stacked_widget.addWidget(launcher)
    stacked_widget.show()
    sys.exit(app.exec())