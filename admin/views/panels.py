import json
import os
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QListWidget, QPushButton,
                             QHBoxLayout, QFormLayout, QLineEdit, QLabel, QSlider,
                             QFontComboBox, QMessageBox, QListWidgetItem, QDialog, QFileDialog, QColorDialog)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt
from .dialogs.auth import ChangePasswordDialog
from .dialogs.category import CategoryEditor
from .dialogs.app import AppEditor


from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTabWidget, QMessageBox, QDialog
from .dialogs.auth_manager import AuthManager, RegistrationDialog, LoginDialog
import os


class AdminPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.data_dir = "data"
        self.categories_file = os.path.join(self.data_dir, "categories.json")
        self.apps_file = os.path.join(self.data_dir, "apps.json")
        self.settings_file = os.path.join(self.data_dir, "settings.json")

        # Проверка авторизации для доступа к админ-панели
        if not self.authenticate_user():
            # Если авторизация неуспешна, закрываем админ-панель
            self.close()
            return

        self.init_ui()

    def authenticate_user(self):
        """Проверяет пользователя и запускает регистрацию или авторизацию."""
        if not AuthManager.user_exists():
            # Если пользователь еще не зарегистрирован, запускаем регистрацию
            registration_dialog = RegistrationDialog(parent=self)
            if registration_dialog.exec() != QDialog.DialogCode.Accepted:
                return False
        else:
            # Если пользователь уже зарегистрирован, запускаем авторизацию
            login_dialog = LoginDialog(parent=self)
            if login_dialog.exec() != QDialog.DialogCode.Accepted:
                return False
        return True

    def init_ui(self):
        """Инициализация интерфейса админ-панели"""
        layout = QVBoxLayout()

        self.tabs = QTabWidget()

        # Вкладки админ-панели (категории, приложения, настройки)
        self.categories_tab = QWidget()
        self.init_categories_tab()
        self.tabs.addTab(self.categories_tab, "Категории")

        self.apps_tab = QWidget()
        self.init_apps_tab()
        self.tabs.addTab(self.apps_tab, "Приложения")

        self.settings_tab = QWidget()
        self.init_settings_tab()
        self.tabs.addTab(self.settings_tab, "Настройки")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def init_ui(self):
        """Инициализация интерфейса админ-панели"""
        layout = QVBoxLayout()

        self.tabs = QTabWidget()

        # Вкладки админ-панели (категории, приложения, настройки)
        self.categories_tab = QWidget()
        self.init_categories_tab()
        self.tabs.addTab(self.categories_tab, "Категории")

        self.apps_tab = QWidget()
        self.init_apps_tab()
        self.tabs.addTab(self.apps_tab, "Приложения")

        self.settings_tab = QWidget()
        self.init_settings_tab()
        self.tabs.addTab(self.settings_tab, "Настройки")

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def init_categories_tab(self):
        """Инициализация вкладки категорий"""
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
        pass

    def init_apps_tab(self):
        """Инициализация вкладки приложений"""
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
        pass

    def init_settings_tab(self):
        """Инициализация вкладки настроек"""
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

        self.settings_tab.setLayout(layout)
        self.load_settings()
        pass

    # --------------------
    # Категории
    # --------------------


    def load_categories(self):
        """Загрузка списка категорий из JSON"""
        self.categories_list.clear()
        try:
            with open(self.categories_file, "r", encoding="utf-8") as file:
                categories = json.load(file)
            for category in categories:
                item = QListWidgetItem(category["name"])
                item.setData(Qt.ItemDataRole.UserRole, category["id"])
                self.categories_list.addItem(item)
        except (FileNotFoundError, json.JSONDecodeError):
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить категории!")

    def save_categories(self, categories):
        """Сохранение списка категорий в JSON"""
        try:
            with open(self.categories_file, "w", encoding="utf-8") as file:
                json.dump(categories, file, indent=4, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить категории: {e}")

    def add_category(self):
        """Добавление новой категории"""
        dialog = CategoryEditor(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_categories()

    def edit_category(self):
        """Редактирование выбранной категории"""
        selected = self.categories_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию для редактирования!")
            return

        cat_id = selected.data(Qt.ItemDataRole.UserRole)
        dialog = CategoryEditor(category_id=cat_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_categories()

    def delete_category(self):
        """Удаление выбранной категории"""
        selected = self.categories_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите категорию для удаления!")
            return

        cat_id = selected.data(Qt.ItemDataRole.UserRole)
        try:
            with open(self.categories_file, "r", encoding="utf-8") as file:
                categories = json.load(file)
            categories = [cat for cat in categories if cat["id"] != cat_id]
            self.save_categories(categories)
            self.load_categories()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить категорию: {e}")

    # --------------------
    # Приложения
    # --------------------



    def load_apps(self):
        """Загрузка списка приложений из JSON"""
        self.apps_list.clear()
        try:
            with open(self.apps_file, "r", encoding="utf-8") as file:
                apps = json.load(file)
            for app in apps:
                item_text = f"{app['name']} ({app.get('category_id', 'Без категории')})"
                item = QListWidgetItem(item_text)
                item.setData(Qt.ItemDataRole.UserRole, app["id"])
                self.apps_list.addItem(item)
        except (FileNotFoundError, json.JSONDecodeError):
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить приложения!")

    def save_apps(self, apps):
        """Сохранение списка приложений в JSON"""
        try:
            with open(self.apps_file, "w", encoding="utf-8") as file:
                json.dump(apps, file, indent=4, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить приложения: {e}")

    def add_app(self):
        """Добавление нового приложения"""
        dialog = AppEditor(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_apps()

    def edit_app(self):
        """Редактирование выбранного приложения"""
        selected = self.apps_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите приложение для редактирования!")
            return

        app_id = selected.data(Qt.ItemDataRole.UserRole)
        dialog = AppEditor(app_id=app_id, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_apps()

    def delete_app(self):
        """Удаление выбранного приложения"""
        selected = self.apps_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите приложение для удаления!")
            return

        app_id = selected.data(Qt.ItemDataRole.UserRole)
        try:
            with open(self.apps_file, "r", encoding="utf-8") as file:
                apps = json.load(file)
            apps = [app for app in apps if app["id"] != app_id]
            self.save_apps(apps)
            self.load_apps()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить приложение: {e}")

    # --------------------
    # Настройки
    # --------------------

    def load_settings(self):
        """Загрузка настроек из JSON"""
        try:
            with open(self.settings_file, "r", encoding="utf-8") as file:
                settings = json.load(file)

            # Проверяем, что загруженные данные — это словарь
            if not isinstance(settings, dict):
                raise ValueError("Формат файла настроек должен быть объектом (словарем).")

            # Установка значений из настроек
            self.bg_image_input.setText(settings.get("background_image", ""))
            bg_color = settings.get("background_color", "#FFFFFF")
            self.bg_color_preview.setStyleSheet(f"background-color: {bg_color};")
            self.bg_color_preview.color = bg_color
            self.opacity_slider.setValue(int(settings.get("opacity", 0.9) * 100))
            self.font_combo.setCurrentText(settings.get("font_family", "Arial"))
        except FileNotFoundError:
            QMessageBox.warning(self, "Ошибка", "Файл настроек не найден!")
        except json.JSONDecodeError:
            QMessageBox.critical(self, "Ошибка", "Файл настроек имеет неверный формат JSON!")
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка в данных настроек: {e}")

    def save_settings(self):
        """Сохранение настроек в JSON"""
        bg_image = self.bg_image_input.text().strip()
        bg_color = getattr(self.bg_color_preview, 'color', "#FFFFFF")
        opacity = self.opacity_slider.value() / 100
        font_family = self.font_combo.currentText()

        settings = {
            "background_image": bg_image,
            "background_color": bg_color,
            "opacity": opacity,
            "font_family": font_family
        }
        try:
            with open(self.settings_file, "w", encoding="utf-8") as file:
                json.dump(settings, file, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "Сохранено", "Настройки успешно сохранены!")
            if self.main_window:
                self.main_window.apply_settings()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить настройки: {e}")

    def browse_bg_image(self):
        """Выбор фонового изображения"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите фоновое изображение", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.bg_image_input.setText(file_path)

    def choose_bg_color(self):
        """Выбор цвета фона"""
        color = QColorDialog.getColor()
        if color.isValid():
            self.bg_color_preview.setStyleSheet(f"background-color: {color.name()};")
            self.bg_color_preview.color = color.name()

    def change_password(self):
        """Изменение пароля администратора"""
        dialog = ChangePasswordDialog(parent=self)
        dialog.exec()