import hashlib
import secrets
import json
from typing import Optional, Tuple
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from utils.json_utils import load_json, save_json
from utils.helpers import resource_path


class AdminLoginDialog(QDialog):
    """Диалоговое окно авторизации администратора"""
    login_success = pyqtSignal(str)  # Сигнал об успешной авторизации

    def __init__(self, auth_controller, parent=None):
        super().__init__(parent)
        self.auth_controller = auth_controller
        self.setWindowTitle("Авторизация администратора")
        self.setFixedSize(350, 220)
        self.setup_ui()

    def setup_ui(self):
        """Инициализация интерфейса"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Заголовок
        title = QLabel("Вход администратора")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        # Поля ввода
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Введите имя пользователя")
        self.username_input.setMinimumHeight(35)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Введите пароль")
        self.password_input.setMinimumHeight(35)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Кнопка входа
        self.login_btn = QPushButton("Войти")
        self.login_btn.setMinimumHeight(40)
        self.login_btn.setStyleSheet(
            "background-color: #4CAF50; color: white; border: none;"
        )

        # Компоновка
        layout.addWidget(title)
        layout.addWidget(QLabel("Имя пользователя:"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("Пароль:"))
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)

        self.setLayout(layout)

        # Обработчики событий
        self.login_btn.clicked.connect(self.attempt_login)
        self.password_input.returnPressed.connect(self.attempt_login)

    def attempt_login(self):
        """Попытка авторизации"""
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            self.show_error("Введите имя пользователя и пароль.")
            return

        if self.auth_controller.authenticate(username, password):
            self.login_success.emit(username)
            self.accept()
        else:
            self.show_error("Неверные учетные данные!")

    def show_error(self, message: str):
        """Показать сообщение об ошибке"""
        QMessageBox.warning(
            self,
            "Ошибка аутентификации",
            message,
            QMessageBox.StandardButton.Ok
        )


class AuthController:
    """Контроллер для управления аутентификацией"""
    def __init__(self, json_path: str = None):
        self.json_file = json_path or resource_path("data/admins.json")
        self._init_json()

    def _init_json(self):
        """Инициализация файла JSON для хранения администраторов"""
        admins = load_json(self.json_file)
        if admins is None:
            # Если файл отсутствует или пустой, создается администратор по умолчанию
            admins = []
            self.create_admin("admin", "admin123")
        elif not admins:
            # Если файл пуст (например, "[]"), создается администратор по умолчанию
            self.create_admin("admin", "admin123")

    @staticmethod
    def _generate_salt() -> str:
        """Генерация криптографической соли"""
        return secrets.token_hex(32)

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        """Хеширование пароля с солью"""
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000,  # Количество итераций
            dklen=128  # Длина ключа
        ).hex()

    def create_admin(self, username: str, password: str) -> bool:
        """Создание нового администратора"""
        if not username or not password:
            return False

        admins = load_json(self.json_file) or []
        if any(admin["username"] == username for admin in admins):
            return False  # Администратор с таким именем уже существует

        salt = self._generate_salt()
        hashed_password = self._hash_password(password, salt)

        admins.append({
            "username": username,
            "password": hashed_password,
            "salt": salt,
            "is_active": True
        })
        save_json(self.json_file, admins)
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Аутентификация администратора"""
        admins = load_json(self.json_file) or []
        for admin in admins:
            if admin["username"] == username and admin["is_active"]:
                salt = admin["salt"]
                stored_hash = admin["password"]
                input_hash = self._hash_password(password, salt)
                return secrets.compare_digest(stored_hash, input_hash)
        return False

    def change_password(self, username: str, current_password: str, new_password: str) -> bool:
        """Безопасная смена пароля"""
        if not self.authenticate(username, current_password):
            return False

        admins = load_json(self.json_file) or []
        for admin in admins:
            if admin["username"] == username:
                salt = self._generate_salt()
                new_hashed = self._hash_password(new_password, salt)
                admin["password"] = new_hashed
                admin["salt"] = salt
                save_json(self.json_file, admins)
                return True
        return False

    def get_admin_count(self) -> int:
        """Получение количества активных администраторов"""
        admins = load_json(self.json_file) or []
        return sum(1 for admin in admins if admin["is_active"])

    def create_login_dialog(self, parent=None) -> AdminLoginDialog:
        """Создание диалога авторизации"""
        return AdminLoginDialog(self, parent)