import sys

from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication

class CommandWindow(QMainWindow):

    def __init__(self, app):

        super().__init__()

        self.app=app

        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )

        stl='''
            QWidget {
                color: white;
                border-color: transparent;
                background-color: transparent;
                }
               ''' 
        self.setStyleSheet(stl)
