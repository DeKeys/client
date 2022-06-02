from PyQt5.QtWidgets import QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtCore import QUrl, QByteArray
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest

from gui.src.widgets.password_list_widget_item import PasswordListWidgetItem

import requests


class PasswordsListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # Create and set font for items
        self.font = QFont()
        self.font.setPointSize(16)
        self.setFont(self.font)

        item1 = PasswordListWidgetItem("https://google.com")
        item2 = PasswordListWidgetItem("https://vk.com")
        self.addItem(item1)
        self.addItem(item2)

        # Create network manager for making requests to the API
        self.networkManager = QNetworkAccessManager()
        self.networkManager.finished.connect(self.completeGetPasswords)
        request = QNetworkRequest(QUrl("http://217.28.228.66:8000/api/get_passwords"))
        self.networkManager.get(request)

    def completeGetPasswords(self, reply):
        status_code = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
        print(status_code)

