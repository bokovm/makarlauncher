import sqlite3

def get_all_apps():
    conn = sqlite3.connect('launcher.db')
    c = conn.cursor()
    c.execute("SELECT a.id, a.name, a.path, c.name, a.icon_path, a.bg_color, a.is_square FROM apps a LEFT JOIN categories c ON a.category_id = c.id")
    apps = c.fetchall()
    conn.close()
    return apps

def get_apps_by_category(category_id):
    conn = sqlite3.connect('launcher.db')
    c = conn.cursor()
    c.execute("SELECT id, name, path, icon_path, bg_color, is_square FROM apps WHERE category_id=? ORDER BY name", (category_id,))
    apps = c.fetchall()
    conn.close()
    return apps

def add_app(name, path, category_id, icon_path=None, bg_color=None, is_square=False):
    conn = sqlite3.connect('launcher.db')
    c = conn.cursor()
    c.execute("INSERT INTO apps (name, path, category_id, icon_path, bg_color, is_square) VALUES (?, ?, ?, ?, ?, ?)",
              (name, path, category_id, icon_path, bg_color, 1 if is_square else 0))
    conn.commit()
    conn.close()

def update_app(app_id, name, path, category_id, icon_path=None, bg_color=None, is_square=False):
    conn = sqlite3.connect('launcher.db')
    c = conn.cursor()
    c.execute("UPDATE apps SET name=?, path=?, category_id=?, icon_path=?, bg_color=?, is_square=? WHERE id=?",
              (name, path, category_id, icon_path, bg_color, 1 if is_square else 0, app_id))
    conn.commit()
    conn.close()

def delete_app(app_id):
    conn = sqlite3.connect('launcher.db')
    c = conn.cursor()
    c.execute("DELETE FROM apps WHERE id=?", (app_id,))
    conn.commit()
    conn.close()