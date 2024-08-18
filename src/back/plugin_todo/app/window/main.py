from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..docks import Docks
from ..display import Display
from ..plugin import Configure
from ..statusbar import StatusBar

class MainWindow(QMainWindow):

    viewCreated=pyqtSignal(object)
    
    def __init__(self, app, display_class=None, view_class=None):

        super().__init__()

        self.app=app
        self.configure=Configure(app, 'Window', self)

        self.setUI(display_class, view_class)

    def setDisplay(self, display_class, view_class=None):

        if not display_class: display_class=Display
        self.display=display_class(self.app, self, view_class)
        self.display.viewCreated.connect(self.viewCreated)
        self.setCentralWidget(self.display)

    def setUI(self, display_class, view_class):

        # Order matters
        self.setDisplay(display_class, view_class)
        self.docks=Docks(self)
        self.bar=StatusBar(self)

        self.setStatusBar(self.bar)

        stl='''
            QWidget {
                color: white;
                border-color: transparent;
                background-color: transparent;
                }
               ''' 
        self.setStyleSheet(stl)
        self.setAcceptDrops(True)
        self.setContentsMargins(2, 2, 2, 2)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def close(self): self.app.exit()

    def open(self, filePath, how='reset', focus=True): 

        data=self.app.buffer.load(filePath)
        self.display.open(data, how, focus)
