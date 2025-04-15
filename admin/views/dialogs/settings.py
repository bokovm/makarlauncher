from PyQt6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QPushButton,
                             QColorDialog, QFileDialog, QMessageBox)
from PyQt6.QtGui import QColor
from admin.controllers.settings import SettingsController


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.settings = SettingsController.get_settings()
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout()

        # Фоновое изображение
        self.bg_image_input = QLineEdit(self.settings[0] if self.settings[0] else "")
        self.bg_image_btn = QPushButton("Выбрать...")
        self.bg_image_btn.clicked.connect(self.select_bg_image)

        # Цвет фона
        self.bg_color_input = QLineEdit(self.settings[1] if self.settings[1] else "")
        self.bg_color_btn = QPushButton("Выбрать...")
        self.bg_color_btn.clicked.connect(self.select_bg_color)

        # Прозрачность
        self.opacity_input = QLineEdit(str(self.settings[2]) if self.settings[2] else "")

        # Шрифт
        self.font_input = QLineEdit(self.settings[3] if self.settings[3] else "")

        # Кнопки
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)

        # Добавляем элементы в layout
        layout.addRow("Фоновое изображение:", self.bg_image_input)
        layout.addRow("", self.bg_image_btn)
        layout.addRow("Цвет фона:", self.bg_color_input)
        layout.addRow("", self.bg_color_btn)
        layout.addRow("Прозрачность (0.1-1.0):", self.opacity_input)
        layout.addRow("Шрифт:", self.font_input)
        layout.addRow(self.save_btn, self.cancel_btn)

        self.setLayout(layout)
        self.setWindowTitle("Настройки лаунчера")
        self.setFixedSize(400, 300)

    def select_bg_image(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Выберите фоновое изображение",
            "", "Images (*.png *.jpg *.jpeg)")
        if filename:
            self.bg_image_input.setText(filename)

    def select_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.bg_color_input.setText(color.name())

    def save_settings(self):
        try:
            opacity = float(self.opacity_input.text())
            if not 0.1 <= opacity <= 1.0:
                raise ValueError("Opacity must be between 0.1 and 1.0")

            success = SettingsController.update_settings(
                background_image=self.bg_image_input.text() or None,
                background_color=self.bg_color_input.text() or None,
                opacity=opacity,
                font_family=self.font_input.text() or None
            )

            if success:
                QMessageBox.information(self, "Успех", "Настройки сохранены!")
                self.accept()
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось сохранить настройки")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Некорректные данные: {str(e)}")