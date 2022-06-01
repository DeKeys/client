from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel, QLineEdit, QCheckBox
from PyQt6.QtGui import QFont


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
        self.submitPasswordButton.setText("Submit")
        self.submitPasswordButton.setDefault(True)

        # Text box
        self.passwordOpenButton = QCheckBox()

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

