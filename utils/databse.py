import sqlite3
import hashlib


def init_db():
    conn = sqlite3.connect('launcher.db')
    c = conn.cursor()

    # Таблица категорий
    c.execute('''CREATE TABLE IF NOT EXISTS categories
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  icon_path TEXT,
                  sort_order INTEGER)''')

    # Таблица приложений
    c.execute('''CREATE TABLE IF NOT EXISTS apps
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  path TEXT NOT NULL,
                  category_id INTEGER,
                  icon_path TEXT,
                  bg_color TEXT,
                  is_square INTEGER DEFAULT 0,
                  FOREIGN KEY(category_id) REFERENCES categories(id))''')

    # Таблица настроек
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                 (id INTEGER PRIMARY KEY,
                  background_image TEXT,
                  background_color TEXT DEFAULT '#333333',
                  opacity REAL DEFAULT 0.9,
                  font_family TEXT DEFAULT 'Arial',
                  admin_password TEXT)''')

    # Проверяем наличие администратора
    c.execute("SELECT COUNT(*) FROM settings WHERE id=1")
    if c.fetchone()[0] == 0:
        # Устанавливаем пароль по умолчанию (хеш от 'admin')
        default_pass = hashlib.sha256('admin'.encode()).hexdigest()
        c.execute("INSERT INTO settings (id, admin_password) VALUES (1, ?)", (default_pass,))

    conn.commit()
    conn.close()


init_db()