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

