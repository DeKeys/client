from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout

from gui.src.widgets.passwords_list_header import PasswordsListHeader
from gui.src.widgets.passwords_list_widget import PasswordsListWidget


class Ui_PasswordsListWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.resize(700, 500)

        self.setWindowTitle("DeKeys")

        # Create central widget and layout
        self.centralWidget = QWidget()
        self.gridLayout = QGridLayout()

        # Create header and widget for listing passwords
        self.header = PasswordsListHeader(self)
        self.passwordsList = PasswordsListWidget(self)

        # Add widgets to the layout
        self.gridLayout.addWidget(self.header, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.passwordsList, 1, 0, 1, 1)

        # Set margin to zero
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        # Add layout to central widget and set new central widget
        self.centralWidget.setLayout(self.gridLayout)
        self.setCentralWidget(self.centralWidget)

