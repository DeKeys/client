from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont, QMovie
from PyQt5.QtCore import QSize, Qt
import os


class Ui_PasswordsListHeader(QWidget):
    """Password List Header"""
    def __init__(self, parent=None):
        """Load widget"""
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
        self.addPasswordButton.setMaximumWidth(100)

        # Button for deleting password
        self.deletePasswordButton = QPushButton()
        self.deletePasswordButton.setText("Delete")
        self.deletePasswordButton.setMaximumWidth(100)

        self.refreshPasswordsButton = QPushButton()
        self.refreshPasswordsButton.setText("Refresh")
        self.refreshPasswordsButton.setMaximumWidth(100)

        # Load spinner gif
        self.spinner = QMovie(os.path.join("gui", "assets", "spinner.gif"))
        self.spinner.setCacheMode(QMovie.CacheAll)
        self.spinner.setSpeed(100)
        self.spinner.setScaledSize(QSize(24, 24))

        # Loading indicator
        self.loadingIndicator = QLabel()
        self.loadingIndicator.setMovie(self.spinner)

        # Add widgets to layout
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.loadingIndicator, 0, 1, 1, 1, alignment=Qt.AlignRight)
        self.gridLayout.addWidget(self.addPasswordButton, 0, 2, 1, 1)
        self.gridLayout.addWidget(self.deletePasswordButton, 0, 3, 1, 1)
        self.gridLayout.addWidget(self.refreshPasswordsButton, 0, 4, 1, 1)

        self.setLayout(self.gridLayout)

