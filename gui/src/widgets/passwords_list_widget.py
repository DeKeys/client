from PyQt6.QtWidgets import QListWidget, QListWidgetItem
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtCore import QUrl
from PyQt6.QtNetwork import QNetworkAccessManager, QNetworkRequest

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
        self.networkManager.finished.connect(self.complete_get_passwords)
        request = QNetworkRequest(QUrl("http://217.28.228.66:8000/api/get_passwords"))
        self.networkManager.get(request).readAll()

    def complete_get_passwords(self, reply):
        print(reply.readAll())
