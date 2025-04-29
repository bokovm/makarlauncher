import json
from PyQt6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QPushButton,
                             QVBoxLayout, QLabel, QFileDialog, QMessageBox, QSpinBox, QHBoxLayout)


class CategoryEditor(QDialog):
    def __init__(self, category_id=None, parent=None):
        super().__init__(parent)
        self.category_id = category_id
        self.setWindowTitle("Редактирование категории" if category_id else "Добавление категории")
        self.setFixedSize(400, 250)

        # Основной интерфейс
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

        # Загрузка данных категории, если есть ID
        if category_id:
            self.load_category_data()

        self.setLayout(layout)

    def browse_icon(self):
        """Выбор иконки для категории"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите иконку", "", "Images (*.png *.jpg *.ico)")
        if file_path:
            self.icon_path_input.setText(file_path)

    def load_category_data(self):
        """Загрузка данных категории из JSON"""
        try:
            with open("categories.json", "r", encoding="utf-8") as file:
                categories = json.load(file)

            category = next((cat for cat in categories if cat["id"] == self.category_id), None)
            if category:
                self.name_input.setText(category["name"])
                self.icon_path_input.setText(category.get("icon_path", ""))
                self.sort_order_input.setValue(category.get("sort_order", 1))
        except (FileNotFoundError, json.JSONDecodeError):
            QMessageBox.critical(self, "Ошибка", "Не удалось загрузить данные категории!")

    def save_category(self):
        """Сохранение категории в JSON"""
        name = self.name_input.text().strip()
        icon_path = self.icon_path_input.text().strip()
        sort_order = self.sort_order_input.value()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Название категории не может быть пустым!")
            return

        try:
            # Загрузка существующих категорий
            try:
                with open("categories.json", "r", encoding="utf-8") as file:
                    categories = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError):
                categories = []

            # Обновление или добавление категории
            if self.category_id:
                for category in categories:
                    if category["id"] == self.category_id:
                        category["name"] = name
                        category["icon_path"] = icon_path
                        category["sort_order"] = sort_order
                        break
            else:
                new_id = max((cat["id"] for cat in categories), default=0) + 1
                categories.append({
                    "id": new_id,
                    "name": name,
                    "icon_path": icon_path,
                    "sort_order": sort_order
                })

            # Сохранение данных в JSON
            with open("categories.json", "w", encoding="utf-8") as file:
                json.dump(categories, file, indent=4, ensure_ascii=False)

            QMessageBox.information(self, "Успех", "Категория успешно сохранена!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить категорию: {e}")