from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .main import MainWindow

from plugin.widget import StackWidget

class StackWindow(QMainWindow):

    def __init__(self, app):

        super().__init__()

        self.app=app
        self.stack=StackWidget()
        self.setCentralWidget(self.stack)

        self.setUI()

        self.show()
        
    def setUI(self):

        self.app.main=MainWindow(self.app)
        self.add(self.app.main, 'main', main=True)

        stl='''
            QWidget {
                color: #101010;
                border-color: #101010;
                background-color: #101010;
                }
               ''' 

        self.setStyleSheet(stl)

    def add(self, *args, **kwargs):

        self.stack.addWidget(*args, **kwargs)

    def show(self, *args, **kwargs):

        super().show()
        self.stack.show(*args, **kwargs)
