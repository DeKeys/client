from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont


class PasswordsListHeader(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.gridLayout = QGridLayout()

        # Create bold font
        self.boldFont = QFont()
        self.boldFont.setWeight(500)
        self.boldFont.setPointSize(20)

        # Title label
        self.titleLabel = QLabel("Your passwords")
        self.titleLabel.setFont(self.boldFont)

        # Button for adding password
        self.addPasswordButton = QPushButton()
        self.addPasswordButton.setText("Add")

        # Button for editing password
        self.editPasswordButton = QPushButton()
        self.editPasswordButton.setText("Edit")

        # Button for deleting password
        self.deletePasswordButton = QPushButton()
        self.deletePasswordButton.setText("Delete")

        # Add widgets to layout
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.addPasswordButton, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.editPasswordButton, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.deletePasswordButton, 0, 3, 1, 1)

        self.setLayout(self.gridLayout)

