import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .docks import Docks
from .buffer import Buffer
from .display import Display
from .statusbar import StatusBar

from lura.utils import Configure, register, getBoundaries

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
                border-color: #101010;
                background-color: #101010;
                }
               ''' 
        self.setStyleSheet(stl)
        self.setAcceptDrops(True)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.show()

    def openBy(self, kind, criteria):
 
        dhash=None

        if kind=='hash':
            filePath=self.app.tables.hash.getPath(criteria)
            self.open(filePath)

        elif kind=='annotation':
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
            print(data)
            if data:
                data=data[0]
                dhash=data['hash']
                page=data['page']
                x, y=(float(i) for i in data['position'].split(':'))

        if dhash:
            self.openBy(kind='hash', criteria=dhash)
            view=self.app.window.display.currentView()
            if view: view.jumpToPage(page, x, y)

    @register('o', modes=['normal', 'command'])
    def open(self, filePath=None, how='reset', focus=True):

        filePath=os.path.abspath(filePath)
        document=self.buffer.loadDocument(filePath)
        if document: self.display.open(document, how, focus=focus)

    @register('q', modes=['normal', 'command'])
    def close(self): super().close()

    @register('ffj')
    def focusLeftDock(self): self.docks.focus('left')

    @register('ffl')
    def focusRightDock(self): self.docks.focus('right')

    @register('ffk')
    def focusTopDock(self): self.docks.focus('top')

    @register('ffh')
    def focusBottomDock(self): self.docks.focus('bottom')

    @register(key='ffc')
    def focusCurrentView(self): self.display.setFocus()

    @register(key='ffu')
    def focusUpView(self): self.display.focusUp()

    @register(key='ffd')
    def focusDownView(self): self.display.focusDown()
