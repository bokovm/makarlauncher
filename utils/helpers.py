import os
import sys
import hashlib
import secrets
from typing import Optional


def resource_path(relative_path: str) -> str:
    """
    Получение абсолютного пути к ресурсу.
    Работает как при разработке, так и в собранном приложении (PyInstaller).
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller создает временную папку
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def generate_secure_token(length: int = 32) -> str:
    """Генерация криптографически безопасного токена"""
    return secrets.token_hex(length)


def validate_password(password: str) -> bool:
    """Проверка сложности пароля"""
    if len(password) < 8:
        return False
    # Дополнительные проверки можно добавить здесь
    return True


def get_app_data_dir(app_name: str = "MakarLauncher") -> str:
    """
    Возвращает путь к директории данных приложения
    """
    if sys.platform == "win32":
        path = os.path.join(os.getenv('APPDATA'), app_name)
    elif sys.platform == "darwin":
        path = os.path.join(os.path.expanduser('~/Library/Application Support'), app_name)
    else:
        path = os.path.join(os.path.expanduser('~/.local/share'), app_name)

    os.makedirs(path, exist_ok=True)
    return path