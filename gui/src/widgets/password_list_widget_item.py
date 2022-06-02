from PyQt5.QtWidgets import QListWidgetItem
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

import requests
import os


def getIconFromUrl(url: str) -> QIcon:
    pixmap = QPixmap()
    pixmap.loadFromData(requests.get(url + "/favicon.ico").content)
    icon = QIcon()
    icon.addPixmap(pixmap)
    return icon


class PasswordListWidgetItem(QListWidgetItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create network access manager for getting icon
        self.network_access_manager = QNetworkAccessManager()
        self.network_access_manager.finished.connect(self.finished_getting_icon)

        # Get icon from specified url
        request = QNetworkRequest(QUrl(self.text() + "/favicon.ico"))
        self.network_access_manager.get(request)

        self.pixmap = QPixmap(os.path.join("gui", "assets", "link.png"))
        self.icon = QIcon()
        self.icon.addPixmap(self.pixmap)
        self.setIcon(self.icon)

    def finished_getting_icon(self, reply):
        status_code = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
        if status_code == 200:
            self.pixmap = QPixmap()
            self.icon = QIcon()
            self.pixmap.loadFromData(reply.readAll())
            self.icon.addPixmap(self.pixmap)
            self.setIcon(self.icon)
