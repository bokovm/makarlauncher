from utils.json_utils import load_json, save_json


def get_settings(file_path="data/settings.json"):
    """Получить текущие настройки"""
    settings = load_json(file_path)
    if settings is None:
        settings = {
            "background_image": None,
            "background_color": None,
            "opacity": 1.0,
            "font_family": "Arial",
            "admin_password": None
        }
        save_json(file_path, settings)
    return settings


def update_settings(background_image=None, background_color=None, opacity=None, font_family=None, admin_password=None, file_path="data/settings.json"):
    """Обновить настройки"""
    settings = get_settings(file_path)
    if background_image is not None:
        settings["background_image"] = background_image
    if background_color is not None:
        settings["background_color"] = background_color
    if opacity is not None:
        settings["opacity"] = opacity
    if font_family is not None:
        settings["font_family"] = font_family
    if admin_password is not None:
        settings["admin_password"] = admin_password
    save_json(file_path, settings)