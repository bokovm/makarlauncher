import os
import webbrowser
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                             QHBoxLayout, QMessageBox)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize
from utils.json_utils import load_json, save_json


class BrowserMenu(QWidget):
    def __init__(self, switch_to, is_admin=False):
        super().__init__()
        self.switch_to = switch_to
        self.is_admin = is_admin  # Флаг администратора
        self.sites_file = "data/sites.json"  # Путь к JSON файлу с сайтами
        self.init_ui()
        self.setup_styles()
        self.load_sites()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.layout = QVBoxLayout()
        self.layout.setSpacing(15)
        self.layout.setContentsMargins(30, 30, 30, 30)

        # Заголовок
        self.title = QLabel("Браузер и сайты")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title)

        # Контейнер для списка сайтов
        self.sites_container = QWidget()
        self.sites_layout = QVBoxLayout()
        self.sites_container.setLayout(self.sites_layout)
        self.layout.addWidget(self.sites_container)

        # Кнопка "Назад"
        self.back_btn = QPushButton("Назад")
        self.back_btn.clicked.connect(lambda: self.switch_to("main"))
        self.layout.addWidget(self.back_btn)

        # Кнопка "Добавить сайт" (только для админа)
        if self.is_admin:
            self.add_btn = QPushButton("Добавить сайт")
            self.add_btn.clicked.connect(self.add_site_dialog)
            self.layout.addWidget(self.add_btn)

        self.setLayout(self.layout)

    def setup_styles(self):
        """Устанавливает стили для всех элементов"""
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(40, 40, 40, 0.8);
            }
        """)

        self.title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
        """)

        self.button_style = """
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
        """

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

        if hasattr(self, 'add_btn'):
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

    def load_sites(self):
        """Загрузка сайтов из JSON файла"""
        sites = load_json(self.sites_file) or []

        # Очищаем текущий список
        for i in reversed(range(self.sites_layout.count())):
            item = self.sites_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        # Добавляем сайты
        if not sites:
            self.show_info_message("Информация", "Список сайтов пуст!")
        for site in sites:
            self.add_site_button(site)

    def add_site_button(self, site):
        """Добавляет кнопку сайта в интерфейс"""
        btn_layout = QHBoxLayout()

        # Основная кнопка сайта
        site_btn = QPushButton(site.get("name", "Без имени"))
        site_btn.setStyleSheet(self.button_style)

        if site.get("icon_path") and os.path.exists(site["icon_path"]):
            site_btn.setIcon(QIcon(site["icon_path"]))
            site_btn.setIconSize(QSize(32, 32))

        site_btn.clicked.connect(lambda _, u=site.get("url", ""): self.open_site(u))
        btn_layout.addWidget(site_btn, stretch=1)

        # Кнопки редактирования (только для админа)
        if self.is_admin:
            edit_btn = QPushButton("✏")
            edit_btn.setToolTip("Редактировать")
            edit_btn.clicked.connect(lambda: self.edit_site(site))
            btn_layout.addWidget(edit_btn)

            delete_btn = QPushButton("🗑")
            delete_btn.setToolTip("Удалить")
            delete_btn.clicked.connect(lambda: self.delete_site(site))
            btn_layout.addWidget(delete_btn)

        self.sites_layout.addLayout(btn_layout)

    def open_site(self, url):
        """Открывает сайт в браузере по умолчанию"""
        if not url:
            self.show_error_message("Ошибка", "URL не указан!")
            return
        try:
            webbrowser.open(url)
        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось открыть сайт:\n{str(e)}")

    def add_site_dialog(self):
        """Диалог добавления нового сайта"""
        sites = load_json(self.sites_file) or []
        new_site = {"id": len(sites) + 1, "name": "Новый сайт", "url": "", "icon_path": ""}
        sites.append(new_site)
        save_json(self.sites_file, sites)
        self.load_sites()

    def edit_site(self, site):
        """Редактирование существующего сайта (заглушка)"""
        self.show_info_message("Редактирование", f"Редактирование сайта: {site['name']}")

    def delete_site(self, site):
        """Удаление сайта"""
        reply = QMessageBox.question(
            self, 'Подтверждение',
            f'Вы уверены, что хотите удалить сайт: {site.get('name', 'Без имени')}?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            sites = load_json(self.sites_file) or []
            sites = [s for s in sites if s["id"] != site["id"]]
            save_json(self.sites_file, sites)
            self.load_sites()

    def show_error_message(self, title, message):
        """Показать сообщение об ошибке"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()

    def show_info_message(self, title, message):
        """Показать информационное сообщение"""
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.exec()