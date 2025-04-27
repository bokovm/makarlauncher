import logging
import os
import re
import secrets
import sys
from typing import Any


def setup_logging(log_level=logging.INFO, log_file='launcher.log'):
    """Настройка системы логирования"""
    try:
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, mode='a', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        logging.info("Логирование настроено")
    except Exception as e:
        print(f"[ERROR] Ошибка при настройке логирования: {e}")


def resource_path(relative_path: str) -> str:
    """Получение абсолютного пути к ресурсу"""
    try:
        # Проверка, используется ли PyInstaller
        base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
        full_path = os.path.join(base_path, relative_path)
        logging.info(f"Сформирован путь к ресурсу: {full_path}")
        return full_path
    except Exception as e:
        logging.error(f"Ошибка при обработке пути: {e}")
        raise


def generate_secure_token(length: int = 32) -> str:
    """Генерация криптографически безопасного токена"""
    try:
        if length <= 0:
            raise ValueError("Длина токена должна быть положительным числом.")
        token = secrets.token_hex(length)
        logging.info(f"Сгенерирован безопасный токен длиной {length} символов.")
        return token
    except Exception as e:
        logging.error(f"Ошибка при генерации токена: {e}")
        raise


def validate_password(password: str) -> bool:
    """Проверка сложности пароля"""
    try:
        if len(password) < 8:
            logging.warning("Пароль слишком короткий. Минимальная длина — 8 символов.")
            return False
        if not re.search(r'[A-Z]', password):  # Заглавная буква
            logging.warning("Пароль должен содержать хотя бы одну заглавную букву.")
            return False
        if not re.search(r'[0-9]', password):  # Цифра
            logging.warning("Пароль должен содержать хотя бы одну цифру.")
            return False
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):  # Спец. символ
            logging.warning("Пароль должен содержать хотя бы один специальный символ.")
            return False
        logging.info("Пароль соответствует требованиям безопасности.")
        return True
    except Exception as e:
        logging.error(f"Ошибка при проверке пароля: {e}")
        return False


def get_app_data_dir(app_name: str = "MakarLauncher") -> str:
    """
    Возвращает путь к директории данных приложения
    """
    try:
        if sys.platform == "win32":
            appdata = os.getenv('APPDATA')
            if not appdata:
                raise EnvironmentError("Переменная окружения APPDATA не найдена.")
            path = os.path.join(appdata, app_name)
        elif sys.platform == "darwin":
            path = os.path.join(os.path.expanduser('~/Library/Application Support'), app_name)
        else:
            path = os.path.join(os.path.expanduser('~/.local/share'), app_name)

        # Создаём директорию, если она не существует
        os.makedirs(path, exist_ok=True)
        logging.info(f"Директория данных приложения: {path}")
        return path
    except Exception as e:
        logging.error(f"Ошибка при создании директории данных приложения: {e}")
        raise

def resource_path(relative_path):
    """Возвращает абсолютный путь к ресурсу"""
    base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)