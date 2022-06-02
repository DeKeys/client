from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import QUrl, QByteArray

from gui.ui.passwords_list_window import Ui_PasswordsListWindow
from gui.src.widgets.password_list_widget_item import PasswordListWidgetItem
from gui.constants import private_key, public_key, pub_key_string
from gui.utils import generate_verification

from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

import json
import secrets
from binascii import unhexlify


class PasswordsListWindow(Ui_PasswordsListWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Create network manager
        self.getNetworkManager = QNetworkAccessManager()
        self.getNetworkManager.finished.connect(self.finishedGettingPasswords)

        self.deleteNetworkManager = QNetworkAccessManager()
        self.deleteNetworkManager.finished.connect(self.finishedDeletingPassword)

        self.header.refreshPasswordsButton.clicked.connect(self.getPasswords)
        self.header.deletePasswordButton.clicked.connect(self.deletePasswords)

        self.passwords = []

        self.getPasswords()

    def deletePasswords(self):
        for index in self.passwordsList.selectedIndexes():
            request = QNetworkRequest(QUrl("http://217.28.228.66:8000/api/delete_password"))
            request.setHeader(QNetworkRequest.ContentTypeHeader, "application/json")
            pwd = self.passwords[index.row()]
            data, signature = generate_verification()
            self.deleteNetworkManager.post(request, QByteArray(json.dumps({
                "verification_string": data,
                "signature": signature,
                "public_key": pub_key_string,
                "address": pwd["address"]
            }).encode("utf-8")))

    def getPasswords(self):
        # Create requests for getting passwords
        self.header.loadingIndicator.setHidden(False)
        self.header.spinner.start()
        request = QNetworkRequest(QUrl("http://217.28.228.66:8000/api/get_passwords"))
        data, signature = generate_verification()
        self.getNetworkManager.sendCustomRequest(
            request, 
            QByteArray("GET".encode("utf-8")), 
            QByteArray(json.dumps({
                "public_key": pub_key_string, 
                "verification_string": data, 
                "signature": signature
            }).encode("utf-8"))
        )

    def finishedDeletingPassword(self, reply):
        self.getPasswords()

    def finishedGettingPasswords(self, reply):
        try:
            encrypted_passwords = json.loads(json.loads(bytes(reply.readAll()).decode("utf-8")))
            res = []
            self.passwordsList.clear()
            if encrypted_passwords:
                for pwd in encrypted_passwords["passwords"]:
                    pwd["service"] = private_key.decrypt(
                        unhexlify(pwd["service"]),
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA512()),
                            algorithm=hashes.SHA512(),
                            label=None
                        )
                    ).decode("utf-8")
                    pwd["login"] = private_key.decrypt(
                        unhexlify(pwd["login"]),
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA512()),
                            algorithm=hashes.SHA512(),
                            label=None
                        )
                    ).decode("utf-8")
                    pwd["password"] = private_key.decrypt(
                        unhexlify(pwd["password"]),
                        padding.OAEP(
                            mgf=padding.MGF1(algorithm=hashes.SHA512()),
                            algorithm=hashes.SHA512(),
                            label=None
                        )
                    ).decode("utf-8")
                    res.append(pwd)
                    self.passwordsList.addItem(PasswordListWidgetItem(pwd["service"]))
                self.passwords = res
                self.header.spinner.stop()
                self.header.loadingIndicator.setHidden(True)
        except json.decoder.JSONDecodeError:
            pass
