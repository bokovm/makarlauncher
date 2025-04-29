from db_handler import DBHandler

class UserManager:
    def __init__(self, db_file):
        self.db = DBHandler(db_file)

    def add_user(self, username, user_data):
        if self.db.get(username):
            raise ValueError("Пользователь уже существует")
        self.db.set(username, user_data)

    def remove_user(self, username):
        if not self.db.get(username):
            raise ValueError("Пользователь не найден")
        self.db.delete(username)

    def get_user(self, username):
        return self.db.get(username)

    def update_user(self, username, user_data):
        if not self.db.get(username):
            raise ValueError("Пользователь не найден")
        self.db.set(username, user_data)