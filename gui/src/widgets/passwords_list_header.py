from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont

from gui.ui.passwords_list_header import Ui_PasswordsListHeader

from gui.src.windows.password_addition_window import PasswordAdditionWindow


class PasswordsListHeader(Ui_PasswordsListHeader):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.addPasswordButton.clicked.connect(self.addPassword)

    def addPassword(self):
        addPasswordWindow = PasswordAdditionWindow({
            "service": "",
            "login": "",
            "password": ""
        }, parent=self)
        addPasswordWindow.show()
