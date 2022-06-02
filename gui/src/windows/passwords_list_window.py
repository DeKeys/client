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
    def __init__(self):
        super().__init__()

        # Create network manager
        self.networkManager = QNetworkAccessManager()
        self.networkManager.finished.connect(self.finishedGettingPasswords)

        # Create requests for getting passwords
        request = QNetworkRequest(QUrl("http://217.28.228.66:8000/api/get_passwords"))
        data, signature = generate_verification()
        self.networkManager.sendCustomRequest(
            request, 
            QByteArray("GET".encode("utf-8")), 
            QByteArray(json.dumps({
                "public_key": pub_key_string, 
                "verification_string": data, 
                "signature": signature
            }).encode("utf-8"))
        )

        self.passwords = []

    def finishedGettingPasswords(self, reply):
        try:
            encrypted_passwords = json.loads(json.loads(bytes(reply.readAll()).decode("utf-8")))
            res = []
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