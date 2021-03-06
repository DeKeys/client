from PyQt5.QtWidgets import QLineEdit, QMessageBox
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl, QByteArray

from gui.ui.password_modification_window import Ui_PasswordModificationWindow

from gui.constants import pub_key_string, public_key, private_key
from gui.utils import generate_verification

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

import json


class PasswordAdditionWindow(Ui_PasswordModificationWindow):
    """Class addition key window"""
    def __init__(self, data, parent=None):
        """Load window"""
        super().__init__(data, parent=parent)

        self.networkManager = QNetworkAccessManager()
        self.networkManager.finished.connect(self.finishedAddingPassword)

        self.data = data
        self.submitPasswordButton.clicked.connect(self.buttonSubmitPressed)
        self.submitPasswordButton.setText("Add")

    def finishedAddingPassword(self, reply):
        """Func which finish add key"""
        statusCode = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
        if statusCode == 200:
            self.parent().parent.getPasswords()
            msg = QMessageBox(self)
            msg.setText("Successfully added password")
            msg.show()
            self.close()
        else:
            msg = QMessageBox(self)
            msg.setText("Couldn't add password")
            msg.setInformativeText("Check your internet connection")
            msg.show()

    def buttonSubmitPressed(self):
        """Func for button Submit, work with server"""
        service = self.serviceLineEdit.text()
        login = self.loginLineEdit.text()
        password = self.passwordLineEdit.text()
        enc_login = public_key.encrypt(
            login.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA512()),
                algorithm=hashes.SHA512(),
                label=None
            )
        ).hex()
        enc_service = public_key.encrypt(
            service.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA512()),
                algorithm=hashes.SHA512(),
                label=None
            )
        ).hex()
        enc_password = public_key.encrypt(
            password.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA512()),
                algorithm=hashes.SHA512(),
                label=None
            )
        ).hex()
        request = QNetworkRequest(QUrl("http://217.28.228.66:8000/api/create_password"))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        verification_string, signature = generate_verification()
        data = {
            "service": enc_service, 
            "login": enc_login, 
            "password": enc_password,
            "verification_string": verification_string,
            "signature": signature,
            "public_key": pub_key_string
        }
        self.networkManager.post(request, QByteArray(json.dumps(data).encode("utf-8")))


