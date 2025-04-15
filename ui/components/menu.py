from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                             QHBoxLayout, QMessageBox)
from PyQt6.QtCore import Qt
import sqlite3
import os
import webbrowser


class MainMenu(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.init_ui()

    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.update_layout()

    def update_layout(self):
        # Очищаем текущий layout
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Добавляем заголовок
        title = QLabel("Главное меню")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: white;")
        self.layout.addWidget(title)

        # Загружаем категории и приложения
        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()

        # Получаем категории в порядке сортировки
        c.execute("SELECT id, name, icon_path FROM categories ORDER BY sort_order")
        categories = c.fetchall()

        for cat_id, cat_name, cat_icon in categories:
            # Добавляем категорию
            category_label = QLabel(cat_name)
            category_label.setStyleSheet("font-size: 20px; color: white; margin-top: 20px;")
            self.layout.addWidget(category_label)

            # Получаем приложения для этой категории
            c.execute(
                "SELECT id, name, path, icon_path, bg_color, is_square FROM apps WHERE category_id=? ORDER BY name",
                (cat_id,))
            apps = c.fetchall()

            # Создаем контейнер для приложений
            apps_container = QWidget()
            apps_layout = QHBoxLayout()
            apps_container.setLayout(apps_layout)

            for app_id, app_name, app_path, app_icon, bg_color, is_square in apps:
                app_btn = QPushButton()
                app_btn.setToolTip(app_name)

                # Настройка внешнего вида кнопки
                if app_icon and os.path.exists(app_icon):
                    from PyQt6.QtGui import QIcon
                    from PyQt6.QtCore import QSize
                    icon = QIcon(app_icon)
                    app_btn.setIcon(icon)
                    app_btn.setIconSize(QSize(64, 64))

                app_btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: {bg_color if bg_color else 'rgba(70, 130, 180, 0.85)'};
                        border-radius: {'10px' if is_square else '32px'};
                        min-width: 80px;
                        min-height: 80px;
                        border: none;
                    }}
                    QPushButton:hover {{
                        background-color: {bg_color if bg_color else 'rgba(90, 150, 200, 0.9)'};
                    }}
                """)

                # Обработчик клика
                if app_path.startswith(('http://', 'https://')):
                    app_btn.clicked.connect(lambda _, p=app_path: webbrowser.open(p))
                else:
                    app_btn.clicked.connect(lambda _, p=app_path: self.launch_app(p))

                apps_layout.addWidget(app_btn)

            self.layout.addWidget(apps_container)

        conn.close()

        # Добавляем кнопку админ-панели
        admin_btn = QPushButton("Админ-панель")
        admin_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(180, 70, 70, 0.85);
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
                margin-top: 30px;
            }
            QPushButton:hover {
                background-color: rgba(200, 90, 90, 0.9);
            }
        """)
        admin_btn.clicked.connect(self.main_window.show_admin_panel)
        self.layout.addWidget(admin_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.layout.addStretch()

    def launch_app(self, path):
        try:
            os.startfile(path)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось запустить приложение:\n{str(e)}")