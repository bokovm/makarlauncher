from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class MainMenu(QWidget):
    def __init__(self, switch_to, show_admin_auth):
        super().__init__()
        self.switch_to = switch_to
        self.show_admin_auth = show_admin_auth
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(50, 50, 50, 50)

        # Заголовок
        title = QLabel("Главное меню")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 28px;
                font-weight: bold;
                qproperty-alignment: AlignCenter;
            }
        """)
        layout.addWidget(title)

        # Стиль для кнопок
        button_style = """
            QPushButton {
                background-color: rgba(70, 130, 180, 0.85);
                color: white;
                font-size: 20px;
                padding: 15px;
                border-radius: 10px;
                border: 2px solid #4682B4;
                min-width: 250px;
            }
            QPushButton:hover {
                background-color: rgba(90, 150, 200, 0.9);
            }
        """

        # Кнопки меню
        buttons = [
            ("Игры", "games"),
            ("Браузер", "browser"),
            ("Общение", "chat"),
            ("Настройки", "settings"),
        ]

        for label, screen in buttons:
            btn = QPushButton(label)
            btn.setStyleSheet(button_style)
            btn.clicked.connect(lambda _, s=screen: self.switch_to(s))
            layout.addWidget(btn)

        # Кнопка админ-панели (только для авторизованных пользователей)
        admin_btn = QPushButton("Админ-панель")
        admin_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(180, 70, 70, 0.85);
                color: white;
                font-size: 20px;
                padding: 15px;
                border-radius: 10px;
                border: 2px solid #B44646;
                min-width: 250px;
                margin-top: 30px;
            }
            QPushButton:hover {
                background-color: rgba(200, 90, 90, 0.9);
            }
        """)
        admin_btn.clicked.connect(self.show_admin_auth)
        layout.addWidget(admin_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        self.setLayout(layout)