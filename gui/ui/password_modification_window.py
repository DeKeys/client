from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QCheckBox
from PyQt5.QtGui import QFont


class Ui_PasswordModificationWindow(QMainWindow):
    def __init__(self, data, parent=None):
        super().__init__(parent=parent)

        self.centralWidget = QWidget()
        self.gridLayout = QGridLayout()

        self.titleLabelService = QLabel("Service:")

        self.serviceLineEdit = QLineEdit()
        self.serviceLineEdit.setText(data["service"])

        self.titleLabelLogin = QLabel("Login:")

        self.loginLineEdit = QLineEdit()
        self.loginLineEdit.setText(data["login"])

        self.titleLabelPassword = QLabel("Password:")

        self.passwordLineEdit = QLineEdit()
        self.passwordLineEdit.setText(data["password"])
        self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)

        # Button for adding password
        self.submitPasswordButton = QPushButton()
        self.submitPasswordButton.setDefault(True)
        self.submitPasswordButton.setEnabled(False)

        self.serviceLineEdit.textChanged.connect(self.textChanged)
        self.loginLineEdit.textChanged.connect(self.textChanged)
        self.passwordLineEdit.textChanged.connect(self.textChanged)

        # Check box
        self.passwordOpenButton = QCheckBox()
        self.passwordOpenButton.clicked.connect(self.password_open_button_func)

        self.gridLayout.addWidget(self.titleLabelService, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.serviceLineEdit, 2, 0, 1, 2)
        self.gridLayout.addWidget(self.titleLabelLogin, 3, 0, 1, 2)
        self.gridLayout.addWidget(self.loginLineEdit, 4, 0, 1, 2)
        self.gridLayout.addWidget(self.titleLabelPassword, 5, 0, 1, 2)
        self.gridLayout.addWidget(self.passwordLineEdit, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.passwordOpenButton, 6, 1, 1, 1)
        self.gridLayout.addWidget(self.submitPasswordButton, 7, 0, 1, 2)

        self.centralWidget.setLayout(self.gridLayout)
        self.setCentralWidget(self.centralWidget)

    def textChanged(self, new):
        self.submitPasswordButton.setEnabled(bool(self.serviceLineEdit.text() and\
                                                  self.loginLineEdit.text() and\
                                                  self.passwordLineEdit.text()))
    def password_open_button_func(self):
        if self.passwordOpenButton.isChecked():
            self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passwordLineEdit.setEchoMode(QLineEdit.EchoMode.Password)


