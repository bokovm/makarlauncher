from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QPushButton


class CategoryEditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QFormLayout()
        self.name_input = QLineEdit()
        self.icon_input = QLineEdit()
        self.save_btn = QPushButton("Save")
        layout.addRow("Name:", self.name_input)
        layout.addRow("Icon:", self.icon_input)
        layout.addRow(self.save_btn)
        self.setLayout(layout)