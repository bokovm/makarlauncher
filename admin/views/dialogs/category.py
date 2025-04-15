from PyQt6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QPushButton,
                             QVBoxLayout, QLabel, QFileDialog, QMessageBox, QSpinBox, QHBoxLayout)
import sqlite3


class CategoryEditor(QDialog):
    def __init__(self, category_id=None, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.setWindowTitle("Редактирование категории" if category_id else "Добавление категории")
        self.setFixedSize(400, 250)

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.icon_path_input = QLineEdit()
        self.icon_path_input.setReadOnly(True)
        self.browse_icon_btn = QPushButton("Выбрать иконку")
        self.browse_icon_btn.clicked.connect(self.browse_icon)
        self.sort_order_input = QSpinBox()
        self.sort_order_input.setRange(1, 100)

        btn_layout = QHBoxLayout()
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save_category)
        self.cancel_btn = QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.cancel_btn)

        layout.addRow("Название:", self.name_input)
        layout.addRow("Иконка:", self.icon_path_input)
        layout.addRow("", self.browse_icon_btn)
        layout.addRow("Порядок сортировки:", self.sort_order_input)
        layout.addRow(btn_layout)

        if category_id:
            self.load_category_data()

        self.setLayout(layout)

    def browse_icon(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите иконку", "", "Images (*.png *.jpg *.ico)")
        if file_path:
            self.icon_path_input.setText(file_path)

    def load_category_data(self):
        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()
        c.execute("SELECT name, icon_path, sort_order FROM categories WHERE id=?", (self.category_id,))
        data = c.fetchone()
        conn.close()

        if data:
            self.name_input.setText(data[0])
            self.icon_path_input.setText(data[1] if data[1] else "")
            self.sort_order_input.setValue(data[2] if data[2] else 1)

    def save_category(self):
        name = self.name_input.text().strip()
        icon_path = self.icon_path_input.text().strip()
        sort_order = self.sort_order_input.value()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Название категории не может быть пустым!")
            return

        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()

        if self.category_id:
            c.execute("UPDATE categories SET name=?, icon_path=?, sort_order=? WHERE id=?",
                      (name, icon_path if icon_path else None, sort_order, self.category_id))
        else:
            c.execute("INSERT INTO categories (name, icon_path, sort_order) VALUES (?, ?, ?)",
                      (name, icon_path if icon_path else None, sort_order))

        conn.commit()
        conn.close()
        self.accept()