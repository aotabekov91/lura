import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .docks import Docks
from .buffer import Buffer
from .display import Display
from .statusbar import StatusBar

from lura.utils import Configure, register, getBoundaries

class MainWindow(QMainWindow):

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
                border-color: transparent;
                background-color: transparent;
                }
               ''' 
        self.setStyleSheet(stl)
        self.setAcceptDrops(True)

        self.setContentsMargins(2, 2, 2, 2)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.show()

    def openBy(self, kind, criteria):
 
        if kind=='hash':

            filePath=self.app.tables.hash.getPath(criteria)
            self.open(filePath)

        else:

            dhash=None
            
            if kind=='annotation':
                data=self.app.tables.annotation.getRow({'id':criteria})
                if data:
                    data=data[0]
                    dhash=data['hash']
                    page=data['page']
                    boundary=getBoundaries(data['position'])[0]
                    topLeft=boundary.topLeft() 
                    x, y = topLeft.x(), topLeft.y()

            elif kind=='bookmark':
                data=self.app.tables.bookmark.getRow({'id':criteria})
                if data:
                    data=data[0]
                    dhash=data['hash']
                    page=data['page']
                    x, y=(float(i) for i in data['position'].split(':'))

            if dhash:

                self.openBy(kind='hash', criteria=dhash)
                view=self.app.main.display.currentView()
                if view: view.jumpToPage(page, x, y)

    def open(self, filePath=None, how='reset', focus=True):

        if filePath:

            filePath=os.path.abspath(filePath)
            document=self.buffer.loadDocument(filePath)
            if document: self.display.open(document, how, focus=focus)

    @register('q', modes=['normal', 'command'])
    def close(self): self.app.exit()
