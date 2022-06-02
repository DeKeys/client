from PyQt5.QtWidgets import QLineEdit

from gui.ui.password_modification_window import Ui_PasswordModificationWindow


class PasswordAdditionWindow(Ui_PasswordModificationWindow):
    def __init__(self, data, parent=None):
        super().__init__(data, parent=parent)

        self.data = data
        self.submitPasswordButton.clicked.connect(self.button_submit_pressed)
        self.submitPasswordButton.setText("Add")

    def button_submit_pressed(self):
        service = self.serviceLineEdit.text()
        login = self.loginLineEdit.text()
        password = self.passwordLineEdit.text()
        if service == data["service"] and login == data["login"] and password == data["password"]:
            PasswordModificationWindow.close(self)
        else:
            self.data = {"service": service, "login": login, "password": password}


