import json
import os


def load_json(file_path):
    """Загружает данные из JSON-файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"[ERROR] Файл {file_path} не найден.")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] Ошибка чтения JSON из {file_path}: {e}")
        return None


def save_json(file_path, data):
    """Сохраняет данные в JSON-файл."""
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] Ошибка записи в файл {file_path}: {e}")