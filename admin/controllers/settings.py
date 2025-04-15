import sqlite3
import hashlib
from typing import Optional, Tuple

class SettingsController:
    @staticmethod
    def get_settings() -> Tuple:
        """Получает текущие настройки из БД"""
        conn = sqlite3.connect('launcher.db')
        c = conn.cursor()
        c.execute("""SELECT background_image, background_color, 
                     opacity, font_family, admin_password 
                     FROM settings WHERE id=1""")
        settings = c.fetchone()
        conn.close()
        return settings

    @staticmethod
    def update_settings(
        background_image: Optional[str] = None,
        background_color: Optional[str] = None,
        opacity: Optional[float] = None,
        font_family: Optional[str] = None
    ) -> bool:
        """Обновляет настройки в БД"""
        try:
            conn = sqlite3.connect('launcher.db')
            c = conn.cursor()
            c.execute("""UPDATE settings SET 
                        background_image=COALESCE(?, background_image),
                        background_color=COALESCE(?, background_color),
                        opacity=COALESCE(?, opacity),
                        font_family=COALESCE(?, font_family)
                        WHERE id=1""",
                    (background_image, background_color, opacity, font_family))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating settings: {e}")
            return False

    @staticmethod
    def change_password(new_password: str) -> bool:
        """Изменяет пароль администратора"""
        try:
            new_hash = hashlib.sha256(new_password.encode()).hexdigest()
            conn = sqlite3.connect('launcher.db')
            c = conn.cursor()
            c.execute("UPDATE settings SET admin_password=? WHERE id=1", (new_hash,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error changing password: {e}")
            return False

    @staticmethod
    def verify_password(password: str) -> bool:
        """Проверяет пароль администратора"""
        try:
            input_hash = hashlib.sha256(password.encode()).hexdigest()
            conn = sqlite3.connect('launcher.db')
            c = conn.cursor()
            c.execute("SELECT admin_password FROM settings WHERE id=1")
            db_password = c.fetchone()[0]
            conn.close()
            return input_hash == db_password
        except Exception as e:
            print(f"Error verifying password: {e}")
            return False