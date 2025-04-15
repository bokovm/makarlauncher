from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import sqlite3
import hashlib


class AdminLoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Вход в админ-панель")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout()

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.verify_password)

        layout.addWidget(QLabel("Введите пароль администратора:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def verify_password(self):
        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()
        c.execute("SELECT admin_password FROM settings WHERE id=1")
        db_password = c.fetchone()[0]
        conn.close()

        input_hash = hashlib.sha256(self.password_input.text().encode()).hexdigest()

        if input_hash == db_password:
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный пароль!")