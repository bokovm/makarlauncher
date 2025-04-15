import hashlib
import secrets
import sqlite3
from typing import Optional, Tuple
from utils.database import Database
from utils.helpers import resource_path


class AuthController:
    def __init__(self, db_path: str = None):
        self.db = Database(db_path or resource_path('launcher.db'))
        self._init_db()

    def _init_db(self):
        """Инициализация таблицы администраторов"""
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS admins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                salt TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.db.commit()

        # Создаем администратора по умолчанию если нет пользователей
        if not self.get_admin_count():
            self.create_admin('admin', 'admin123')

    @staticmethod
    def _generate_salt() -> str:
        """Генерация криптографической соли"""
        return secrets.token_hex(32)

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        """Хеширование пароля с солью"""
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()

    def create_admin(self, username: str, password: str) -> bool:
        """Создание нового администратора"""
        salt = self._generate_salt()
        hashed_password = self._hash_password(password, salt)

        try:
            self.db.execute(
                'INSERT INTO admins (username, password, salt) VALUES (?, ?, ?)',
                (username, hashed_password, salt)
            )
            return self.db.commit()
        except sqlite3.IntegrityError:
            return False

    def authenticate(self, username: str, password: str) -> bool:
        """Аутентификация администратора"""
        result = self.db.execute(
            'SELECT password, salt FROM admins WHERE username = ?',
            (username,)
        )
        row = result.fetchone()

        if not row:
            return False

        stored_hash, salt = row
        input_hash = self._hash_password(password, salt)
        return secrets.compare_digest(stored_hash, input_hash)

    def change_password(self, username: str, new_password: str) -> bool:
        """Смена пароля администратора"""
        salt = self._generate_salt()
        new_hashed = self._hash_password(new_password, salt)

        self.db.execute(
            'UPDATE admins SET password = ?, salt = ? WHERE username = ?',
            (new_hashed, salt, username)
        )
        return self.db.commit()

    def get_admin_count(self) -> int:
        """Получение количества администраторов"""
        result = self.db.execute('SELECT COUNT(*) FROM admins')
        return result.fetchone()[0]

    def get_admin_info(self, username: str) -> Optional[Tuple]:
        """Получение информации об администраторе"""
        result = self.db.execute(
            'SELECT id, username, created_at FROM admins WHERE username = ?',
            (username,)
        )
        return result.fetchone()