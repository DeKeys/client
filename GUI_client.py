from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont

from gui.src.windows.passwords_list_window import PasswordsListWindow

import sys


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = PasswordsListWindow()
    main.show()
    app.exec()
