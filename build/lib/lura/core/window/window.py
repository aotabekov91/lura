from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import classify

from ..actions import Actions

from .components.buffer import Buffer
from .components.docks import Docks
from .components.display import Display
from .components.statusbar import StatusBar

class Window(QMainWindow):

    keyPressEventOccurred=pyqtSignal(object)

    def __init__(self, app):
        super().__init__()

        self.app=app

        self.documents={}
        self.buffer=Buffer(self.app)

        # Order matters
        self.docks=Docks(self)
        self.statusbar=StatusBar(self.app)
        self.setStatusBar(self.statusbar)
        self.display=Display(self.app)
        self.setCentralWidget(self.display)

        stl='''
            QWidget {
                color: white;
                border-width: 0px;
                border-color: transparent;
                background-color: transparent;
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

    def setActions(self):
        self.actions=Actions(self.app, 'Window', self)
        self.display.setActions()
        self.statusbar.setActions()
        self.docks.setActions()

    def open(self, filePath=None, how='reset', focus=True):
        document=self.buffer.loadDocument(filePath)
        if document: 
            self.display.open(document, how, focus=focus)

    def keyPressEvent(self, event):
        self.keyPressEventOccurred.emit(event)

    @classify(context=Qt.WindowShortcut)
    def close(self):
        super().close()
