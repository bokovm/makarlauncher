import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from core.launcher import Launcher
import sqlite3
import hashlib


def init_db():
    """Инициализация базы данных при запуске приложения"""
    conn = sqlite3.connect('launcher.db')
    c = conn.cursor()

    # Создаем таблицу настроек, если ее нет
    c.execute("""CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY,
                background_image TEXT,
                background_color TEXT DEFAULT '#333333',
                opacity REAL DEFAULT 0.9,
                font_family TEXT DEFAULT 'Arial',
                admin_password TEXT)""")

    # Проверяем наличие записи с настройками
    c.execute("SELECT COUNT(*) FROM settings WHERE id=1")
    if c.fetchone()[0] == 0:
        # Устанавливаем пароль по умолчанию (хеш от 'admin')
        default_pass = hashlib.sha256('admin'.encode()).hexdigest()
        c.execute("INSERT INTO settings (id, admin_password) VALUES (1, ?)",
                  (default_pass,))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Инициализируем базу данных перед запуском приложения
    init_db()

    # Создаем и настраиваем приложение
    app = QApplication(sys.argv)
    stacked_widget = QStackedWidget()
    launcher = Launcher(stacked_widget)
    stacked_widget.addWidget(launcher)

    # Показываем окно в полноэкранном режиме
    stacked_widget.showFullScreen()

    # Запускаем главный цикл приложения
    sys.exit(app.exec())