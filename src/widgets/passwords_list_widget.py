from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

import requests


def getIconFromUrl(url: str) -> QIcon:
    pixmap = QPixmap()
    pixmap.loadFromData(requests.get(url + "/favicon.ico").content)
    icon = QIcon()
    icon.addPixmap(pixmap)
    return icon


class PasswordsListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Create font for items
        self.font = QFont()
        self.font.setPointSize(14)

        self.networkManager = QNetworkAccessManager()
        self.networkManager.finished.connect(self.complete_get_passwords)
        request = QNetworkRequest(QUrl("http://217.28.228.66:8000/api/get_passwords"))
        self.networkManager.get(request).readAll())

        self.setFont(self.font)
    
    def complete_get_passwords(self, reply):
        print(reply.readAll())
