import logging
import os
import re
import secrets
import sys
from typing import Any


def setup_logging(log_level=logging.INFO):
    """Настройка системы логирования"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('launcher.log', mode='a'),
            logging.StreamHandler()
        ]
    )
    logging.info("Логирование настроено")


def resource_path(relative_path: str) -> str:
    """Получение абсолютного пути к ресурсу"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    try:
        return os.path.join(base_path, relative_path)
    except Exception as e:
        logging.error(f"Ошибка при обработке пути: {e}")
        raise


def generate_secure_token(length: int = 32) -> str:
    """Генерация криптографически безопасного токена"""
    if length <= 0:
        raise ValueError("Длина токена должна быть положительным числом.")
    return secrets.token_hex(length)


def validate_password(password: str) -> bool:
    """Проверка сложности пароля"""
    if len(password) < 8:
        logging.warning("Пароль слишком короткий")
        return False
    if not re.search(r'[A-Z]', password):  # Заглавная буква
        logging.warning("Пароль должен содержать хотя бы одну заглавную букву")
        return False
    if not re.search(r'[0-9]', password):  # Цифра
        logging.warning("Пароль должен содержать хотя бы одну цифру")
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # Спец. символ
        logging.warning("Пароль должен содержать хотя бы один специальный символ")
        return False
    return True


def get_app_data_dir(app_name: str = "MakarLauncher") -> str:
    """
    Возвращает путь к директории данных приложения
    """
    if sys.platform == "win32":
        appdata = os.getenv('APPDATA')
        if not appdata:
            raise EnvironmentError("Переменная окружения APPDATA не найдена.")
        path = os.path.join(appdata, app_name)
    elif sys.platform == "darwin":
        path = os.path.join(os.path.expanduser('~/Library/Application Support'), app_name)
    else:
        path = os.path.join(os.path.expanduser('~/.local/share'), app_name)

    os.makedirs(path, exist_ok=True)
    logging.info(f"Директория данных приложения: {path}")
    return path