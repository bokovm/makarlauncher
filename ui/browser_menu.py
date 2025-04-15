import os

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                             QHBoxLayout, QMessageBox, QInputDialog)
from PyQt6.QtGui import QFont, QIcon, QPixmap
from PyQt6.QtCore import Qt, QSize
import webbrowser
import sqlite3
from admin.views.dialogs.app import AppEditor  # Для редактирования сайтов


class BrowserMenu(QWidget):
    def __init__(self, switch_to, is_admin=False):
        super().__init__()
        self.switch_to = switch_to
        self.is_admin = is_admin  # Флаг администратора
        self.init_ui()
        self.setup_styles()
        self.load_sites_from_db()  # Загрузка сайтов из БД

    def init_ui(self):
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

        # Стиль заголовка
        self.title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 24px;
                font-weight: bold;
                padding: 10px;
            }
        """)

        # Общий стиль для кнопок сайтов
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

        # Стиль кнопки "Назад"
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

        # Стиль кнопки "Добавить сайт"
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

    def load_sites_from_db(self):
        """Загрузка сайтов из базы данных"""
        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()

        # Получаем сайты из категории "Браузер" (category_id=3)
        c.execute("""SELECT id, name, path, icon_path FROM apps 
                     WHERE category_id=3 ORDER BY name""")
        sites = c.fetchall()
        conn.close()

        # Очищаем текущий список
        for i in reversed(range(self.sites_layout.count())):
            self.sites_layout.itemAt(i).widget().setParent(None)

        # Добавляем сайты
        for site_id, name, url, icon_path in sites:
            self.add_site_button(site_id, name, url, icon_path)

    def add_site_button(self, site_id, name, url, icon_path=None):
        """Добавляет кнопку сайта в интерфейс"""
        btn_layout = QHBoxLayout()

        # Основная кнопка сайта
        site_btn = QPushButton(name)
        site_btn.setStyleSheet(self.button_style)

        if icon_path and os.path.exists(icon_path):
            site_btn.setIcon(QIcon(icon_path))
            site_btn.setIconSize(QSize(32, 32))

        site_btn.clicked.connect(lambda _, u=url: self.open_site(u))
        btn_layout.addWidget(site_btn, stretch=1)

        # Кнопки редактирования (только для админа)
        if self.is_admin:
            edit_btn = QPushButton()
            edit_btn.setIcon(QIcon.fromTheme("edit"))
            edit_btn.setToolTip("Редактировать")
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(180, 180, 50, 0.85);
                    border-radius: 5px;
                    padding: 5px;
                    min-width: 30px;
                    max-width: 30px;
                }
                QPushButton:hover {
                    background-color: rgba(200, 200, 70, 0.9);
                }
            """)
            edit_btn.clicked.connect(lambda _, sid=site_id: self.edit_site(sid))
            btn_layout.addWidget(edit_btn)

            delete_btn = QPushButton()
            delete_btn.setIcon(QIcon.fromTheme("delete"))
            delete_btn.setToolTip("Удалить")
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(180, 50, 50, 0.85);
                    border-radius: 5px;
                    padding: 5px;
                    min-width: 30px;
                    max-width: 30px;
                }
                QPushButton:hover {
                    background-color: rgba(200, 70, 70, 0.9);
                }
            """)
            delete_btn.clicked.connect(lambda _, sid=site_id: self.delete_site(sid))
            btn_layout.addWidget(delete_btn)

        self.sites_layout.addLayout(btn_layout)

    def open_site(self, url):
        """Открывает сайт в браузере по умолчанию"""
        try:
            webbrowser.open(url)
        except Exception as e:
            self.show_error_message("Ошибка", f"Не удалось открыть сайт:\n{str(e)}")

    def add_site_dialog(self):
        """Диалог добавления нового сайта"""
        dialog = AppEditor(category_id=3, parent=self)  # category_id=3 для сайтов
        if dialog.exec():
            self.load_sites_from_db()

    def edit_site(self, site_id):
        """Редактирование существующего сайта"""
        dialog = AppEditor(app_id=site_id, parent=self)
        if dialog.exec():
            self.load_sites_from_db()

    def delete_site(self, site_id):
        """Удаление сайта"""
        reply = QMessageBox.question(
            self, 'Подтверждение',
            'Вы уверены, что хотите удалить этот сайт?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('launcher.db')
            c = conn.cursor()
            c.execute("DELETE FROM apps WHERE id=?", (site_id,))
            conn.commit()
            conn.close()
            self.load_sites_from_db()

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
            }
        """)
        msg.exec()