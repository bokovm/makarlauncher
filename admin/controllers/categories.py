import sqlite3

def get_all_categories():
    conn = sqlite3.connect('launcher.db')
    c = conn.cursor()
    c.execute("SELECT id, name, icon_path, sort_order FROM categories ORDER BY sort_order")
    categories = c.fetchall()
    conn.close()
    return categories

def add_category(name, icon_path=None, sort_order=1):
    conn = sqlite3.connect('launcher.db')
    c = conn.cursor()
    c.execute("INSERT INTO categories (name, icon_path, sort_order) VALUES (?, ?, ?)",
              (name, icon_path, sort_order))
    conn.commit()
    conn.close()

def update_category(category_id, name, icon_path=None, sort_order=1):
    conn = sqlite3.connect('launcher.db')
    c = conn.cursor()
    c.execute("UPDATE categories SET name=?, icon_path=?, sort_order=? WHERE id=?",
              (name, icon_path, sort_order, category_id))
    conn.commit()
    conn.close()

def delete_category(category_id):
    conn = sqlite3.connect('launcher.db')
    c = conn.cursor()
    c.execute("DELETE FROM categories WHERE id=?", (category_id,))
    conn.commit()
    conn.close()