from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager
from PyQt5.QtCore import QUrl, QByteArray

from gui.ui.password_modification_window import Ui_PasswordModificationWindow
from gui.constants import pub_key_string, public_key, private_key
from gui.utils import generate_verification

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

import json


class PasswordModificationWindow(Ui_PasswordModificationWindow):
    def __init__(self, data, parent=None):
        super().__init__(data, parent=parent)

        self.data = data

        self.submitPasswordButton.clicked.connect(self.savePassword)

        self.serviceLineEdit.textChanged.connect(self.checkChange)
        self.loginLineEdit.textChanged.connect(self.checkChange)
        self.passwordLineEdit.textChanged.connect(self.checkChange)

        self.networkManager = QNetworkAccessManager()
        self.networkManager.finished.connect(self.passwordSaved)

        self.submitPasswordButton.setText("Save")

    def passwordSaved(self, reply):
        self.parent().getPasswords()

    def checkChange(self, text):
        service = self.serviceLineEdit.text()
        login = self.loginLineEdit.text()
        password = self.passwordLineEdit.text()
        self.submitPasswordButton.setEnabled(not bool(service == self.data["service"] and\
                                                      login == self.data["login"] and\
                                                      password == self.data["password"]))

    def savePassword(self):
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
        enc_password = public_key.encrypt(
            password.encode("utf-8"),
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
        verification_string, signature = generate_verification()

        request = QNetworkRequest(QUrl("http://217.28.228.66:8000/api/edit_password"))
        request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
        self.networkManager.post(request, QByteArray(json.dumps({
            "public_key": pub_key_string,
            "verification_string": verification_string,
            "signature": signature,
            "address": self.data["address"],
            "service": enc_service,
            "login": enc_login,
            "password": enc_password
        }).encode("utf-8")))

