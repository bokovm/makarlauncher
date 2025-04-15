from PyQt6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QPushButton, QComboBox,
                             QLabel, QFileDialog, QColorDialog, QHBoxLayout, QMessageBox)
from PyQt6.QtGui import QColor
import sqlite3
import os


class AppEditor(QDialog):
    def __init__(self, app_id=None, parent=None):
        super().__init__(parent)
        self.app_id = app_id
        self.setWindowTitle("Редактирование приложения" if app_id else "Добавление приложения")
        self.setFixedSize(500, 350)

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.path_input = QLineEdit()
        self.browse_path_btn = QPushButton("Выбрать файл")
        self.browse_path_btn.clicked.connect(self.browse_path)
        self.category_combo = QComboBox()
        self.load_categories()
        self.icon_path_input = QLineEdit()
        self.icon_path_input.setReadOnly(True)
        self.browse_icon_btn = QPushButton("Выбрать иконку")
        self.browse_icon_btn.clicked.connect(self.browse_icon)
        self.color_btn = QPushButton("Выбрать цвет")
        self.color_btn.clicked.connect(self.choose_color)
        self.color_preview = QLabel()
        self.color_preview.setFixedSize(30, 30)
        self.is_square_check = QPushButton("Квадратная иконка")
        self.is_square_check.setCheckable(True)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_app)
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)

        layout.addRow("Название:", self.name_input)
        layout.addRow("Путь/URL:", self.path_input)
        layout.addRow("", self.browse_path_btn)
        layout.addRow("Категория:", self.category_combo)
        layout.addRow("Иконка:", self.icon_path_input)
        layout.addRow("", self.browse_icon_btn)
        layout.addRow("Цвет фона:", self.color_btn)
        layout.addRow("", self.color_preview)
        layout.addRow("Форма иконки:", self.is_square_check)
        layout.addRow(btn_layout)

        if app_id:
            self.load_app_data()

        self.setLayout(layout)

    def load_categories(self):
        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()
        c.execute("SELECT id, name FROM categories ORDER BY sort_order")
        categories = c.fetchall()
        conn.close()

        self.category_combo.clear()
        for cat_id, name in categories:
            self.category_combo.addItem(name, cat_id)

    def browse_path(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите приложение", "", "Executables (*.exe);;All Files (*)")
        if file_path:
            self.path_input.setText(file_path)
            if not self.name_input.text():
                self.name_input.setText(os.path.splitext(os.path.basename(file_path))[0])

    def browse_icon(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите иконку", "", "Images (*.png *.jpg *.ico)")
        if file_path:
            self.icon_path_input.setText(file_path)

    def choose_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_preview.setStyleSheet(f"background-color: {color.name()};")
            self.color_preview.color = color.name()

    def load_app_data(self):
        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()
        c.execute("SELECT name, path, category_id, icon_path, bg_color, is_square FROM apps WHERE id=?", (self.app_id,))
        data = c.fetchone()
        conn.close()

        if data:
            self.name_input.setText(data[0])
            self.path_input.setText(data[1])

            index = self.category_combo.findData(data[2])
            if index >= 0:
                self.category_combo.setCurrentIndex(index)

            self.icon_path_input.setText(data[3] if data[3] else "")

            if data[4]:
                self.color_preview.setStyleSheet(f"background-color: {data[4]};")
                self.color_preview.color = data[4]

            self.is_square_check.setChecked(bool(data[5]))

    def save_app(self):
        name = self.name_input.text().strip()
        path = self.path_input.text().strip()
        category_id = self.category_combo.currentData()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Название не может быть пустым!")
            return

        if not path:
            QMessageBox.warning(self, "Ошибка", "Путь/URL не может быть пустым!")
            return

        icon_path = self.icon_path_input.text().strip()
        bg_color = getattr(self.color_preview, 'color', None)
        is_square = 1 if self.is_square_check.isChecked() else 0

        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()

        if self.app_id:
            c.execute('''UPDATE apps SET name=?, path=?, category_id=?, 
                         icon_path=?, bg_color=?, is_square=? WHERE id=?''',
                      (name, path, category_id, icon_path if icon_path else None,
                       bg_color, is_square, self.app_id))
        else:
            c.execute('''INSERT INTO apps 
                         (name, path, category_id, icon_path, bg_color, is_square) 
                         VALUES (?, ?, ?, ?, ?, ?)''',
                      (name, path, category_id, icon_path if icon_path else None,
                       bg_color, is_square))

        conn.commit()
        conn.close()
        self.accept()