import json
import hashlib
from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox


class ChangePasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Изменение пароля")
        self.setFixedSize(300, 200)

        # Создание интерфейса
        layout = QFormLayout()

        self.old_pass_input = QLineEdit()
        self.old_pass_input.setPlaceholderText("Текущий пароль")
        self.old_pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.new_pass_input = QLineEdit()
        self.new_pass_input.setPlaceholderText("Новый пароль")
        self.new_pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.confirm_pass_input = QLineEdit()
        self.confirm_pass_input.setPlaceholderText("Подтвердите пароль")
        self.confirm_pass_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.change_btn = QPushButton("Изменить пароль")
        self.change_btn.clicked.connect(self.change_password)

        layout.addRow("Текущий пароль:", self.old_pass_input)
        layout.addRow("Новый пароль:", self.new_pass_input)
        layout.addRow("Подтверждение:", self.confirm_pass_input)
        layout.addRow(self.change_btn)

        self.setLayout(layout)

    def load_admin_password(self):
        """Загрузить текущий хэш пароля администратора из JSON"""
        try:
            with open("settings.json", "r", encoding="utf-8") as file:
                settings = json.load(file)
                return settings.get("admin_password")
        except (FileNotFoundError, json.JSONDecodeError):
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить настройки.")
            return None

    def save_admin_password(self, new_password_hash):
        """Сохранить обновленный хэш пароля администратора в JSON"""
        try:
            with open("settings.json", "r", encoding="utf-8") as file:
                settings = json.load(file)

            settings["admin_password"] = new_password_hash

            with open("settings.json", "w", encoding="utf-8") as file:
                json.dump(settings, file, indent=4)

        except (FileNotFoundError, json.JSONDecodeError):
            QMessageBox.critical(self, "Ошибка", "Не удалось сохранить настройки.")

    def change_password(self):
        """Логика изменения пароля администратора"""
        old_pass = self.old_pass_input.text()
        new_pass = self.new_pass_input.text()
        confirm_pass = self.confirm_pass_input.text()

        if not old_pass or not new_pass or not confirm_pass:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Ошибка", "Новый пароль и подтверждение не совпадают!")
            return

        # Загрузка текущего хэша пароля из JSON
        current_password_hash = self.load_admin_password()
        if current_password_hash is None:
            return

        # Проверка текущего пароля
        old_hash = hashlib.sha256(old_pass.encode()).hexdigest()
        if old_hash != current_password_hash:
            QMessageBox.warning(self, "Ошибка", "Неверный текущий пароль!")
            return

        # Хэширование нового пароля и сохранение его в JSON
        new_hash = hashlib.sha256(new_pass.encode()).hexdigest()
        self.save_admin_password(new_hash)

        QMessageBox.information(self, "Успех", "Пароль успешно изменен!")
        self.accept()