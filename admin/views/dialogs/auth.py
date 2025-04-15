from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox
import sqlite3
import hashlib


class ChangePasswordDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Изменение пароля")
        self.setFixedSize(300, 200)

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

    def change_password(self):
        old_pass = self.old_pass_input.text()
        new_pass = self.new_pass_input.text()
        confirm_pass = self.confirm_pass_input.text()

        if not old_pass or not new_pass or not confirm_pass:
            QMessageBox.warning(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        if new_pass != confirm_pass:
            QMessageBox.warning(self, "Ошибка", "Новый пароль и подтверждение не совпадают!")
            return

        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()
        c.execute("SELECT admin_password FROM settings WHERE id=1")
        db_password = c.fetchone()[0]

        old_hash = hashlib.sha256(old_pass.encode()).hexdigest()
        if old_hash != db_password:
            QMessageBox.warning(self, "Ошибка", "Неверный текущий пароль!")
            conn.close()
            return

        new_hash = hashlib.sha256(new_pass.encode()).hexdigest()
        c.execute("UPDATE settings SET admin_password=? WHERE id=1", (new_hash,))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Успех", "Пароль успешно изменен!")
        self.accept()