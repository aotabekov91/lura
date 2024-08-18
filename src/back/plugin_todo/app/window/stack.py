from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .main import MainWindow
from ..display import Display
from ...widget import StackWidget

class StackWindow(QMainWindow):

    def __init__(self, app, display_class=None, view_class=None):

        super().__init__()

        self.app=app
        self.stack=StackWidget()
        self.setCentralWidget(self.stack)
        self.setUI(display_class, view_class)

    def setUI(self, display_class, view_class):

        stl='''
            QWidget {
                color: #101010;
                border-color: #101010;
                background-color: #101010;
                }
               ''' 

        self.app.main=MainWindow(self.app, display_class, view_class)
        self.add(self.app.main, 'main', main=True)
        self.setStyleSheet(stl)

    def add(self, *args, **kwargs): 

        self.stack.addWidget(*args, **kwargs)

    def remove(self, *args, **kwargs): 

        self.stack.removeWidget(*args, **kwargs)

    def show(self, *args, **kwargs):

        super().show()
        self.stack.show(*args, **kwargs)
