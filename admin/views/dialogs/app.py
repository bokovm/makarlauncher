from user_management import UserManager

def main():
    db_file = 'users.json'
    user_manager = UserManager(db_file)

    while True:
        print("\nМеню:")
        print("1. Добавить пользователя")
        print("2. Удалить пользователя")
        print("3. Показать пользователя")
        print("4. Обновить данные пользователя")
        print("5. Выйти")

        choice = input("Выберите опцию: ")

        if choice == '1':
            username = input("Введите имя пользователя: ")
            user_data = input("Введите данные пользователя: ")
            try:
                user_manager.add_user(username, user_data)
                print("Пользователь добавлен.")
            except ValueError as e:
                print(e)

        elif choice == '2':
            username = input("Введите имя пользователя: ")
            try:
                user_manager.remove_user(username)
                print("Пользователь удален.")
            except ValueError as e:
                print(e)

        elif choice == '3':
            username = input("Введите имя пользователя: ")
            user = user_manager.get_user(username)
            if user:
                print(f"Данные пользователя: {user}")
            else:
                print("Пользователь не найден.")

        elif choice == '4':
            username = input("Введите имя пользователя: ")
            user_data = input("Введите новые данные пользователя: ")
            try:
                user_manager.update_user(username, user_data)
                print("Данные пользователя обновлены.")
            except ValueError as e:
                print(e)

        elif choice == '5':
            print("Выход...")
            break

        else:
            print("Неверный выбор. Пожалуйста, выберите снова.")

if __name__ == "__main__":
    main()