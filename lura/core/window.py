import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .docks import Docks
from .buffer import Buffer
from .display import Display
from .statusbar import StatusBar

from lura.utils import Configure, register

class Window(QMainWindow):

    def __init__(self, app):

        super().__init__()

        self.app=app
        self.documents={}
        self.buffer=Buffer(self.app)
        self.configure=Configure(app, 'Window', self)

        self.setUI()

    def setUI(self):

        # Order matters
        self.display=Display(self.app)

        self.docks=Docks(self)
        self.bar=StatusBar(self)


        self.setStatusBar(self.bar)
        self.setCentralWidget(self.display)

        stl='''
            QWidget {
                color: white;
                border-width: 0px;
                border-color: black;
                background-color: black;
                }
            QWidget#dockWidget {
                background-color: black;
                border-color: black;
                border-width: 2px;
                border-radius: 10px;
                border-style: outset;
                padding: 2px 2px 2px 2px;
                }
            QWidget#centralWidget {
                background-color: transparent;
                border-width: 0px;
                border-style: outset;
                }
            QLabel {
                padding: 0px 10px 0px 0px
                }
            QGraphicsView{
                background-color: transparent;
                color: black;
                border-width: 1px;
                border-radius: 5px;
                border-style: outset;
                }

               ''' 

        self.setStyleSheet(stl)
        self.setAcceptDrops(True)

        self.layout().setSpacing(0)
        self.layout().setContentsMargins(0,0,0,0)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.show()

    @register('o', modes=['normal', 'command'])
    def open(self, filePath=None, how='reset', focus=True):

        filePath=os.path.abspath(filePath)
        document=self.buffer.loadDocument(filePath)
        if document: 
            self.display.open(document, how, focus=focus)

    @register('q', modes=['normal', 'command'])
    def close(self): super().close()
