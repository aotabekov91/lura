from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .viewer import View

from lura.utils import Configure, register

class Display(QSplitter):

    viewCreated=pyqtSignal(object)
    viewChanged=pyqtSignal(object)

    annotationAdded=pyqtSignal(object)
    annotationCreated=pyqtSignal(object)
    annotationRegistered=pyqtSignal(object)

    keyPressEventOccurred=pyqtSignal(object)

    currentPageChanged = pyqtSignal(object, int, int)

    mouseDoubleClickOccured = pyqtSignal(object, object, object)
    mouseReleaseEventOccured = pyqtSignal(object, object, object)
    mouseMoveEventOccured = pyqtSignal(object, object, object)
    mousePressEventOccured = pyqtSignal(object, object, object)
    hoverMoveEventOccured = pyqtSignal(object, object, object)

    # pageItemHasBeenJustCreated = pyqtSignal(object, object)
    pageHasBeenJustPainted = pyqtSignal(object, object, object, object, object)

    def __init__(self, app):

        super().__init__(Qt.Vertical)

        self.app=app

        self.count=-1
        self.views={}
        self.view=None
        self.activated=False

        self.configure=Configure(app, 'Display', self, mode_keys={'command': 'w'})

        # self.style_sheet='''QWidget {background-color: transparent}'''
        # self.setStyleSheet(self.style_sheet)

        self.setup()

    def setup(self):

        # self.m_hsplit=QSplitter(Qt.Vertical)
        # self.m_hsplit.hide()

        self.m_hlayout=QVBoxLayout(self)#.m_hsplit)
        self.m_hlayout.setSpacing(0)
        self.m_hlayout.setContentsMargins(0,0,0,0)

        # layout=QHBoxLayout(self)
        # layout.setSpacing(0)
        # layout.setContentsMargins(0,0,0,0)
        # layout.addWidget(self.m_hsplit)

    def clear(self):

        for index in range(self.m_hlayout.count(),-1, -1):
            item=self.m_hlayout.takeAt(index)
            if item: item.widget().hide()
        self.hide()

    def setView(self, view, how=None, focus=True):

        self.setCurrentView(view)

        if how=='reset':
            self.clear()
            self.m_hlayout.addWidget(view)
            self.show()
        elif how=='below':
            self.m_hlayout.addWidget(view)
            self.show()

        view.show()

        if focus: view.setFocus()

    def addView(self, view):

        self.m_hlayout.addWidget(view)

    def focus(self, increment=1):

        if self.m_hlayout.count()<2:
            view=self.currentView()
            if view: view.setFocus()
        else:
            currentView=self.currentView()
            index=self.indexOf(currentView)
            index+=increment
            if index>=self.m_hlayout.count():
                index=0
            elif index<0:
                index=self.m_hlayout.count()-1
            view=self.widget(index)
            self.setCurrentView(view)
        self.focusCurrentView()

    def closeView(self, view=None, vid=None):

        if view is None:
            view=self.currentView()
        if vid is None and view:
            vid=view.id()
        index=None
        for f in range(self.m_hlayout.count()):
            item=self.m_hlayout.itemAt(f)
            if item and item.widget().id()==vid:
                view=item.widget()
                index=f
                break
        if not index is None:
            self.m_hlayout.removeWidget(view)
            view.close()
            index-=1
            if index<0: index=0
            if self.m_hlayout.count()>0:
                view=self.widget(index)
                self.setCurrentView(view)
                self.focusCurrentView()

    def open(self, document, how='reset', focus=True):

        if how=='rest':
            if self.view and self.view.document()==document: return

        view=self.createView(document)
        self.setView(view, how, focus)

    def createView(self, document):

        view=View(self.app)
        self.count+=1
        view.setId(self.count)
        self.views[self.count]=view
        view.open(document)
        self.viewCreated.emit(view)
        return view

    def currentView(self): return self.view

    def setCurrentView(self, view):

        if view!=self.view: 
            self.view=view
            self.viewChanged.emit(self.view)

    def deactivate(self, focusView=True):

        if self.activated:
            self.activated=False
            statusbar=self.app.main.statusBar()
            statusbar.details.setText('')
            statusbar.hide()
            if focusView: self.focusCurrentView()

    def toggle(self):

        statusbar=self.app.main.statusBar()
        if not self.activated:
            self.activated=True
            statusbar.details.setText(self.configure.name)
            statusbar.show()
            self.show()
            self.setFocus()
        else:
            self.deactivate()

    def keyPressEvent(self, event):

        self.keyPressEventOccurred.emit(event)
        super().keyPressEvent(event)

    @register(key='H', modes=['command'])
    def toggleCursor(self): 

        if self.view: self.view.toggleCursor()

    @register(key='u', modes=['command'])
    def updateView(self): 

        if self.view: self.view.updateAll()

    @register(key='g', modes=['normal'])
    def gotoPage(self, digit=1):

        if self.view: self.view.jumpToPage(digit)

    @register(key='G', modes=['normal'])
    def gotoEnd(self):

        if self.view: self.view.jumpToPage(self.view.document().numberOfPages())

    @register(key='gg', modes=['normal'])
    def gotoBegin(self):

        if self.view: self.view.jumpToPage(1)

    @register(key=']', modes=['normal'])
    def nextPage(self, digit=1): 

        if self.view:
            for d in range(digit): self.view.nextPage()
    
    @register(key='[', modes=['normal'])
    def prevPage(self, digit=1): 

        if self.view:
            for d in range(digit): self.view.prevPage()

    @register(key='K', modes=['normal'])
    def pageUp(self, digit=1): 

        if self.view:
            for d in range(digit): self.view.pageUp()

    @register(key='J', modes=['normal'])
    def pageDown(self, digit=1): 
        
        if self.view:
            for d in range(digit): self.view.pageDown()

    @register(key='k', modes=['normal'])
    def incrementUp(self, digit=1): 

        if self.view:
            for d in range(digit): self.view.incrementUp()

    @register(key='j', modes=['normal'])
    def incrementDown(self, digit=1): 

        if self.view:
            for d in range(digit): self.view.incrementDown()

    @register(key='h', modes=['normal'])
    def incrementLeft(self, digit=1): 

        if self.view:
            for d in range(digit): self.view.incrementLeft()

    @register(key='l', modes=['normal'])
    def incrementRight(self, digit=1): 

        if self.view:
            for d in range(digit): self.view.incrementRight()

    @register(key='zi', modes=['normal'])
    def zoomIn(self, digit=1): 
        
        if self.view:
            for d in range(digit): self.view.zoomIn()

    @register(key='zo', modes=['normal'])
    def zoomOut(self, digit=1): 
        
        if self.view:
            for d in range(digit): self.view.zoomOut()

    @register(key='w', modes=['normal'])
    def fitToPageWidth(self): 

        if self.view: self.view.fitToPageWidth()

    @register(key='s', modes=['normal'])
    def fitToPageHeight(self): 

        if self.view: self.view.fitToPageHeight()

    @register(key='c', modes=['normal'])
    def toggleContinuousMode(self): 

        if self.view: self.view.toggleContinuousMode()

    @register(key='S', modes=['command'])
    def saveDocument(self): 

        if self.view: self.view.save()

    @register(key='X', modes=['normal'])
    def closeCurrentView(self): self.closeView(self.currentView())

    @register('c', modes=['command']) 
    def focusCurrentView(self): 

        self.deactivate(focusView=False)
        self.setFocus()
        if self.view: self.view.setFocus()

    @register('k', modes=['command'])
    def focusUpView(self): self.focus(-1)

    @register('j', modes=['command'])
    def focusDownView(self): self.focus(+1)

    @register('C', modes=['command'])
    def cleanUp(self): 

        if self.view: self.view.cleanUp()
