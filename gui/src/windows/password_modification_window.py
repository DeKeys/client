from PyQt6.QtWidgets import QLineEdit

from gui.ui.password_modification_window import Ui_PasswordModificationWindow


class PasswordModificationWindow(Ui_PasswordModificationWindow):
    def __init__(self, data, parent=None):
        super().__init__(data, parent=parent)

        self.submitPasswordButton.clicked.connect(self.button_submit_pressed)
        self.passwordOpenButton.clicked.connect(self.password_open_button_func)

    def button_submit_pressed(self):
        service = self.serviceLineEdit.text()
        login = self.loginLineEdit.text()
        password = self.passwordLineEdit.text()
        if service == data["service"] and login == data["login"] and password == data["password"]:
            PasswordModificationWindow.close(self)
        else:
            self.data = {"service": service, "login": login, "password": password}
            # Do special func to modification data

    def password_open_button_func(self):
        if self.passwordOpenButton.isChecked():
            self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

