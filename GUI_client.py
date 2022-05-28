from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont
from src.widgets.passwords_list_header import PasswordsListHeader
from src.widgets.passwords_list_widget import PasswordsListWidget
import sys


class PasswordsListWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("DeKeys")

        self.centralWidget = QWidget()
        self.gridLayout = QGridLayout()

        self.header = PasswordsListHeader(self)
        self.passwords_list = PasswordsListWidget(self)

        self.gridLayout.addWidget(self.header, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.passwords_list, 1, 0, 1, 1)

        self.centralWidget.setLayout(self.gridLayout)
        self.setCentralWidget(self.centralWidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = PasswordsListWindow()
    main.show()
    app.exec()
