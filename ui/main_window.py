from PyQt6.QtWidgets import QMainWindow, QStackedWidget, QDialog
from .components.menu import MainMenu
from admin.views.panels import AdminPanel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Лаунчер")
        self.setMinimumSize(800, 600)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.main_menu = MainMenu(self)
        self.admin_panel = AdminPanel(self)

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.admin_panel)

        self.load_settings()
        self.show_main_menu()

    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def show_admin_panel(self):
        from admin.auth import AdminLoginDialog
        dialog = AdminLoginDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.stacked_widget.setCurrentWidget(self.admin_panel)

    def load_settings(self):
        import sqlite3
        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()
        c.execute("SELECT background_image, background_color, opacity, font_family FROM settings WHERE id=1")
        settings = c.fetchone()
        conn.close()

        if settings:
            bg_image, bg_color, opacity, font_family = settings

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

            self.setStyleSheet("QWidget { " + " ".join(style) + " }")

    def apply_settings(self):
        self.load_settings()
        self.main_menu.update_layout()