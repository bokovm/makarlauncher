from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QListWidget, QPushButton,
                             QHBoxLayout, QFormLayout, QLineEdit, QLabel, QSlider,
                             QFontComboBox, QMessageBox, QListWidgetItem, QDialog, QFileDialog, QColorDialog)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from .dialogs.auth import ChangePasswordDialog
from .dialogs.category import CategoryEditor
from .dialogs.app import AppEditor
import sqlite3
import os


class AdminPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.tabs = QTabWidget()

        # Вкладка категорий
        self.categories_tab = QWidget()
        self.init_categories_tab()
        self.tabs.addTab(self.categories_tab, "Категории")

        # Вкладка приложений
        self.apps_tab = QWidget()
        self.init_apps_tab()
        self.tabs.addTab(self.apps_tab, "Приложения")

        # Вкладка настроек
        self.settings_tab = QWidget()
        self.init_settings_tab()
        self.tabs.addTab(self.settings_tab, "Настройки")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def init_categories_tab(self):
        layout = QVBoxLayout()

        self.categories_list = QListWidget()
        self.load_categories()

        btn_layout = QHBoxLayout()
        self.add_category_btn = QPushButton("Добавить")
        self.add_category_btn.clicked.connect(self.add_category)
        self.edit_category_btn = QPushButton("Редактировать")
        self.edit_category_btn.clicked.connect(self.edit_category)
        self.delete_category_btn = QPushButton("Удалить")
        self.delete_category_btn.clicked.connect(self.delete_category)

        btn_layout.addWidget(self.add_category_btn)
        btn_layout.addWidget(self.edit_category_btn)
        btn_layout.addWidget(self.delete_category_btn)

        layout.addWidget(self.categories_list)
        layout.addLayout(btn_layout)

        self.categories_tab.setLayout(layout)

    def init_apps_tab(self):
        layout = QVBoxLayout()

        self.apps_list = QListWidget()
        self.load_apps()

        btn_layout = QHBoxLayout()
        self.add_app_btn = QPushButton("Добавить")
        self.add_app_btn.clicked.connect(self.add_app)
        self.edit_app_btn = QPushButton("Редактировать")
        self.edit_app_btn.clicked.connect(self.edit_app)
        self.delete_app_btn = QPushButton("Удалить")
        self.delete_app_btn.clicked.connect(self.delete_app)

        btn_layout.addWidget(self.add_app_btn)
        btn_layout.addWidget(self.edit_app_btn)
        btn_layout.addWidget(self.delete_app_btn)

        layout.addWidget(self.apps_list)
        layout.addLayout(btn_layout)

        self.apps_tab.setLayout(layout)

    def init_settings_tab(self):
        layout = QFormLayout()

        self.bg_image_input = QLineEdit()
        self.bg_image_input.setReadOnly(True)
        self.browse_bg_btn = QPushButton("Выбрать фон")
        self.browse_bg_btn.clicked.connect(self.browse_bg_image)

        self.bg_color_btn = QPushButton("Выбрать цвет фона")
        self.bg_color_btn.clicked.connect(self.choose_bg_color)
        self.bg_color_preview = QLabel()
        self.bg_color_preview.setFixedSize(30, 30)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(10, 100)
        self.opacity_slider.setValue(90)

        self.font_combo = QFontComboBox()

        self.change_pass_btn = QPushButton("Изменить пароль")
        self.change_pass_btn.clicked.connect(self.change_password)

        self.save_settings_btn = QPushButton("Сохранить настройки")
        self.save_settings_btn.clicked.connect(self.save_settings)

        layout.addRow("Фоновое изображение:", self.bg_image_input)
        layout.addRow("", self.browse_bg_btn)
        layout.addRow("Цвет фона:", self.bg_color_btn)
        layout.addRow("", self.bg_color_preview)
        layout.addRow("Прозрачность:", self.opacity_slider)
        layout.addRow("Шрифт:", self.font_combo)
        layout.addRow("", self.change_pass_btn)
        layout.addRow("", self.save_settings_btn)

        self.load_settings()
        self.settings_tab.setLayout(layout)

    def load_categories(self):
        self.categories_list.clear()
        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()
        c.execute("SELECT id, name FROM categories ORDER BY sort_order")
        categories = c.fetchall()
        conn.close()

        for cat_id, name in categories:
            item = QListWidgetItem(name)
            item.setData(Qt.ItemDataRole.UserRole, cat_id)
            self.categories_list.addItem(item)

    def load_apps(self):
        self.apps_list.clear()
        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()
        c.execute("SELECT a.id, a.name, c.name FROM apps a LEFT JOIN categories c ON a.category_id = c.id")
        apps = c.fetchall()
        conn.close()

        for app_id, app_name, cat_name in apps:
            item = QListWidgetItem(f"{app_name} ({cat_name})" if cat_name else app_name)
            item.setData(Qt.ItemDataRole.UserRole, app_id)
            self.apps_list.addItem(item)

    def load_settings(self):
        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()
        c.execute("SELECT background_image, background_color, opacity, font_family FROM settings WHERE id=1")
        settings = c.fetchone()
        conn.close()

        if settings:
            self.bg_image_input.setText(settings[0] if settings[0] else "")
            if settings[1]:
                self.bg_color_preview.setStyleSheet(f"background-color: {settings[1]};")
                self.bg_color_preview.color = settings[1]
            self.opacity_slider.setValue(int(settings[2] * 100) if settings[2] else 90)
            if settings[3]:
                index = self.font_combo.findText(settings[3])
                if index >= 0:
                    self.font_combo.setCurrentIndex(index)

    def add_category(self):
        dialog = CategoryEditor(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_categories()

    def edit_category(self):
        selected = self.categories_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию для редактирования!")
            return

        cat_id = selected.data(Qt.ItemDataRole.UserRole)
        dialog = CategoryEditor(category_id=cat_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_categories()

    def delete_category(self):
        selected = self.categories_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию для удаления!")
            return

        cat_id = selected.data(Qt.ItemDataRole.UserRole)

        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM apps WHERE category_id=?", (cat_id,))
        apps_count = c.fetchone()[0]
        conn.close()

        if apps_count > 0:
            reply = QMessageBox.question(
                self, "Подтверждение",
                f"В этой категории {apps_count} приложений. Удалить категорию и все связанные приложения?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

            if reply != QMessageBox.StandardButton.Yes:
                return

        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()
        c.execute("DELETE FROM categories WHERE id=?", (cat_id,))
        if apps_count > 0:
            c.execute("DELETE FROM apps WHERE category_id=?", (cat_id,))
        conn.commit()
        conn.close()

        self.load_categories()
        self.load_apps()

    def add_app(self):
        dialog = AppEditor(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_apps()

    def edit_app(self):
        selected = self.apps_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите приложение для редактирования!")
            return

        app_id = selected.data(Qt.ItemDataRole.UserRole)
        dialog = AppEditor(app_id=app_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_apps()

    def delete_app(self):
        selected = self.apps_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите приложение для удаления!")
            return

        app_id = selected.data(Qt.ItemDataRole.UserRole)

        reply = QMessageBox.question(
            self, "Подтверждение",
            "Вы уверены, что хотите удалить это приложение?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            conn = sqlite3.connect('launcher.db')
            c = conn.cursor()
            c.execute("DELETE FROM apps WHERE id=?", (app_id,))
            conn.commit()
            conn.close()

            self.load_apps()

    def browse_bg_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите фоновое изображение", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.bg_image_input.setText(file_path)

    def choose_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.bg_color_preview.setStyleSheet(f"background-color: {color.name()};")
            self.bg_color_preview.color = color.name()

    def change_password(self):
        dialog = ChangePasswordDialog(parent=self)
        dialog.exec()

    def save_settings(self):
        bg_image = self.bg_image_input.text().strip()
        bg_color = getattr(self.bg_color_preview, 'color', None)
        opacity = self.opacity_slider.value() / 100
        font_family = self.font_combo.currentText()

        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()
        c.execute('''UPDATE settings SET 
                     background_image=?, background_color=?, opacity=?, font_family=?
                     WHERE id=1''',
                  (bg_image if bg_image else None, bg_color, opacity, font_family))
        conn.commit()
        conn.close()

        QMessageBox.information(self, "Сохранено", "Настройки успешно сохранены!")
        self.main_window.apply_settings()