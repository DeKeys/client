from PyQt5.QtWidgets import QListWidget
from PyQt5.QtGui import QFont


class PasswordsListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Create font for items
        self.font = QFont()
        self.font.setPointSize(14)

        self.setFont(self.font)

        self.addItems(["test", "tes1", "tes2", "test3"])

