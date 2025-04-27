import json
import os
import hashlib
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox

USER_DATA_FILE = "user_data.json"


class AuthManager:
    @staticmethod
    def hash_password(password):
        """Хэширует пароль для безопасного хранения."""
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def save_user_data(username, password):
        """Сохраняет данные пользователя в JSON-файл."""
        user_data = {
            "username": username,
            "password": AuthManager.hash_password(password)
        }
        with open(USER_DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(user_data, file, indent=4, ensure_ascii=False)

    @staticmethod
    def load_user_data():
        """Загружает данные пользователя из JSON-файла."""
        if not os.path.exists(USER_DATA_FILE):
            return None
        with open(USER_DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def authenticate(username, password):
        """Проверяет логин и пароль пользователя."""
        user_data = AuthManager.load_user_data()
        if not user_data:
            return False
        return (
            username == user_data["username"] and
            AuthManager.hash_password(password) == user_data["password"]
        )

    @staticmethod
    def user_exists():
        """Проверяет, существует ли пользователь."""
        return os.path.exists(USER_DATA_FILE)


class RegistrationDialog(QDialog):
    """Диалог для регистрации нового пользователя."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Регистрация")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите логин")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.register_btn = QPushButton("Зарегистрироваться")
        self.register_btn.clicked.connect(self.register)

        layout.addWidget(QLabel("Регистрация"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_btn)

        self.setLayout(layout)

    def register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Ошибка", "Логин и пароль не могут быть пустыми!")
            return

        AuthManager.save_user_data(username, password)
        QMessageBox.information(self, "Успешно", "Регистрация прошла успешно!")
        self.accept()


class LoginDialog(QDialog):
    """Диалог для авторизации пользователя."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Авторизация")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите логин")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.login)

        layout.addWidget(QLabel("Авторизация"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if AuthManager.authenticate(username, password):
            QMessageBox.information(self, "Успешно", "Вы вошли в систему!")
            self.accept()
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль!")