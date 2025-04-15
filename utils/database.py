import sqlite3
from typing import Optional, Any, List, Dict


class Database:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Выполнение SQL-запроса"""
        try:
            return self.conn.execute(query, params)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise

    def execute_many(self, query: str, params: List[tuple]) -> None:
        """Массовое выполнение запросов"""
        try:
            self.conn.executemany(query, params)
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            raise

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Получение одной записи"""
        cursor = self.execute(query, params)
        result = cursor.fetchone()
        return dict(result) if result else None

    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """Получение всех записей"""
        cursor = self.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def commit(self) -> bool:
        """Фиксация изменений"""
        try:
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Commit error: {e}")
            return False

    def close(self) -> None:
        """Закрытие соединения"""
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.close()