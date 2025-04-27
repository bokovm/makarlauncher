import logging
import os
import re
import secrets
import sys
import json
from typing import Any


def load_json(file_path: str) -> Any:
    """Загружает данные из JSON-файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            logging.info(f"Чтение JSON-файла: {file_path}")
            return json.load(file)
    except FileNotFoundError:
        logging.error(f"Файл {file_path} не найден.")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка чтения JSON из {file_path}: {e}")
        return None
    except Exception as e:
        logging.error(f"Неизвестная ошибка при загрузке JSON из {file_path}: {e}")
        return None


def save_json(file_path: str, data: Any) -> None:
    """Сохраняет данные в JSON-файл."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            logging.info(f"Данные успешно сохранены в файл: {file_path}")
    except Exception as e:
        logging.error(f"Ошибка записи в файл {file_path}: {e}")


def setup_logging(log_level=logging.INFO) -> None:
    """Настройка системы логирования"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('launcher.log', mode='a', encoding='utf-8'),
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
        full_path = os.path.join(base_path, relative_path)
        logging.info(f"Сформирован путь к ресурсу: {full_path}")
        return full_path
    except Exception as e:
        logging.error(f"Ошибка при обработке пути: {e}")
        raise


def generate_secure_token(length: int = 32) -> str:
    """Генерация криптографически безопасного токена"""
    if length <= 0:
        raise ValueError("Длина токена должна быть положительным числом.")
    token = secrets.token_hex(length)
    logging.info(f"Сгенерирован безопасный токен длиной {length} символов.")
    return token


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
    logging.info("Пароль соответствует требованиям безопасности.")
    return True


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

        os.makedirs(path, exist_ok=True)
        logging.info(f"Директория данных приложения: {path}")
        return path
    except Exception as e:
        logging.error(f"Ошибка при создании директории данных приложения: {e}")
        raise