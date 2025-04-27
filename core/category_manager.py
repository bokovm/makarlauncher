import os
from utils.json_utils import load_json, save_json


def get_all_categories(file_path="data/categories.json"):
    """Получить все категории"""
    categories = load_json(file_path)
    if categories is None:
        categories = []
        save_json(file_path, categories)
    return categories


def add_category(name, icon_path=None, sort_order=1, file_path="data/categories.json"):
    """Добавить категорию"""
    categories = get_all_categories(file_path)
    new_id = max((cat["id"] for cat in categories), default=0) + 1
    categories.append({
        "id": new_id,
        "name": name,
        "icon_path": icon_path,
        "sort_order": sort_order
    })
    save_json(file_path, categories)


def update_category(category_id, name, icon_path=None, sort_order=1, file_path="data/categories.json"):
    """Обновить категорию"""
    categories = get_all_categories(file_path)
    for category in categories:
        if category["id"] == category_id:
            category.update({
                "name": name,
                "icon_path": icon_path,
                "sort_order": sort_order
            })
            break
    save_json(file_path, categories)


def delete_category(category_id, file_path="data/categories.json"):
    """Удалить категорию"""
    categories = get_all_categories(file_path)
    categories = [cat for cat in categories if cat["id"] != category_id]
    save_json(file_path, categories)