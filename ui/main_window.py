from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QDialog
from ui.main_menu import MainMenu  # Предполагается, что MainMenu определён в отдельном файле
from admin.views.panels import AdminPanel
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лаунчер")
        self.setMinimumSize(800, 600)

        # Создаем виджет с переключением между экранами
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # Инициализация экранов
        self.main_menu = MainMenu(self.show_admin_panel)
        self.admin_panel = AdminPanel(self)

        # Добавляем экраны в стек
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.admin_panel)

        # Загрузка настроек и отображение главного меню
        self.load_settings()
        self.show_main_menu()

    def show_main_menu(self):
        """Отображение главного меню"""
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def show_admin_panel(self):
        """Отображение панели администратора с авторизацией"""
        from admin.auth import AdminLoginDialog
        dialog = AdminLoginDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.stacked_widget.setCurrentWidget(self.admin_panel)

    def load_settings(self):
        """Загрузка настроек из базы данных и применение их"""
        try:
            with sqlite3.connect('launcher.db') as conn:
                c = conn.cursor()
                c.execute("""
                    SELECT background_image, background_color, opacity, font_family 
                    FROM settings 
                    WHERE id=1
                """)
                settings = c.fetchone()

            if settings:
                bg_image, bg_color, opacity, font_family = settings

                # Формируем стиль в зависимости от данных из настроек
                style = []
                if bg_image:
                    style.append(f"background-image: url({bg_image});")
                    style.append("background-repeat: no-repeat;")
                    style.append("background-position: center;")
                    style.append("background-size: cover;")

                if bg_color:
                    style.append(f"background-color: {bg_color};")

                if opacity:
                    style.append(f"opacity: {opacity};")

                if font_family:
                    style.append(f"font-family: '{font_family}';")

                # Применяем стиль к главному окну
                self.setStyleSheet("QWidget { " + " ".join(style) + " }")

        except sqlite3.Error as e:
            print(f"[ERROR] Ошибка при загрузке настроек: {e}")

    def apply_settings(self):
        """Применение настроек и обновление интерфейса"""
        self.load_settings()
        self.main_menu.update_layout()