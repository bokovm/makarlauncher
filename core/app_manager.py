from utils.json_utils import load_json, save_json


def get_all_apps(file_path="data/apps.json"):
    """Получить все приложения"""
    apps = load_json(file_path)
    if apps is None:
        apps = []
        save_json(file_path, apps)
    return apps


def get_apps_by_category(category_id, file_path="data/apps.json"):
    """Получить приложения по категории"""
    apps = get_all_apps(file_path)
    return [app for app in apps if app["category_id"] == category_id]


def add_app(name, path, category_id, icon_path=None, bg_color=None, is_square=False, file_path="data/apps.json"):
    """Добавить приложение"""
    apps = get_all_apps(file_path)
    new_id = max((app["id"] for app in apps), default=0) + 1
    apps.append({
        "id": new_id,
        "name": name,
        "path": path,
        "category_id": category_id,
        "icon_path": icon_path,
        "bg_color": bg_color,
        "is_square": is_square
    })
    save_json(file_path, apps)


def update_app(app_id, name, path, category_id, icon_path=None, bg_color=None, is_square=False, file_path="data/apps.json"):
    """Обновить приложение"""
    apps = get_all_apps(file_path)
    for app in apps:
        if app["id"] == app_id:
            app.update({
                "name": name,
                "path": path,
                "category_id": category_id,
                "icon_path": icon_path,
                "bg_color": bg_color,
                "is_square": is_square
            })
            break
    save_json(file_path, apps)


def delete_app(app_id, file_path="data/apps.json"):
    """Удалить приложение"""
    apps = get_all_apps(file_path)
    apps = [app for app in apps if app["id"] != app_id]
    save_json(file_path, apps)