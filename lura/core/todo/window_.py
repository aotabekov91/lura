from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .main import MainWindow
from .command import CommandWindow

class Window(QMainWindow):

    def __init__(self, app):

        super().__init__()

        self.app=app
        self.setUI()

    def setUI(self):

        stl='''
            QWidget {
                color: #101010;
                border-color: #101010;
                background-color: #101010;
                }
               ''' 
        self.setStyleSheet(stl)
        self.stack=QStackedWidget()
        self.setCentralWidget(self.stack)

        self.main=MainWindow(self.app)
        self.command=CommandWindow(self.app)

        self.main.sid=self.stack.addWidget(self.main)
        self.command.sid=self.stack.addWidget(self.command)

        self.stack.setCurrentIndex(self.main.sid)


        stl='''
            QWidget {
                color: #101010;
                border-color: transparent;
                background-color: transparent;
                }
               ''' 
        self.stack.setStyleSheet(stl)

        self.show()
