from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton, QMessageBox


class CategoryEditDialog(QDialog):
    def __init__(self, name="", icon="", parent=None):
        """Инициализация диалога редактирования категории.

        Args:
            name (str): Предустановленное имя категории.
            icon (str): Предустановленный путь к иконке категории.
            parent (QWidget): Родительский виджет.
        """
        super().__init__(parent)
        self.name = name
        self.icon = icon
        self.setup_ui()

    def setup_ui(self):
        """Создание интерфейса диалога."""
        self.setWindowTitle("Редактирование категории")
        layout = QFormLayout()

        # Поле для ввода имени
        self.name_input = QLineEdit(self.name)
        self.name_input.setPlaceholderText("Введите название категории")

        # Поле для ввода пути к иконке
        self.icon_input = QLineEdit(self.icon)
        self.icon_input.setPlaceholderText("Введите путь к файлу иконки")

        # Кнопка сохранения
        self.save_btn = QPushButton("Сохранить")
        self.save_btn.clicked.connect(self.save)

        # Добавление элементов в форму
        layout.addRow("Название:", self.name_input)
        layout.addRow("Иконка:", self.icon_input)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def save(self):
        """Обработка сохранения данных."""
        name = self.name_input.text().strip()
        icon = self.icon_input.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Название категории не может быть пустым!")
            return

        # Сохраняем введённые данные и закрываем диалог
        self.name = name
        self.icon = icon
        self.accept()

    def get_data(self):
        """Получение данных из диалога.

        Returns:
            tuple: Кортеж с названием и иконкой категории.
        """
        return self.name, self.icon