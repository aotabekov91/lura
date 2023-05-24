from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .viewer import View

from lura.utils import Configure, register

class Display(QWidget):


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

        super().__init__()

        self.app=app

        self.count=-1
        self.views={}
        self.view=None
        self.activated=False

        self.configure=Configure(app, 'Display', self, mode_keys={'command': 'D'})

        self.style_sheet='''QWidget {background-color: black}'''
        self.setStyleSheet(self.style_sheet)

        self.setup()

    def setup(self):

        self.m_hsplit=QSplitter(Qt.Vertical)
        self.m_hlayout=QVBoxLayout(self.m_hsplit)
        self.m_hlayout.setSpacing(0)
        self.m_hlayout.setContentsMargins(0,0,0,0)

        layout=QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.m_hsplit)

        self.m_hsplit.hide()

    def clear(self):

        for index in range(self.m_hlayout.count(),-1, -1):
            item=self.m_hlayout.takeAt(index)
            if item: item.widget().hide()
        self.m_hsplit.hide()

    def setView(self, view, how=None, focus=True):

        self.setCurrentView(view)

        if how=='reset':
            self.clear()
            self.m_hlayout.addWidget(view)
            self.m_hsplit.show()
        elif how=='below':
            self.m_hlayout.addWidget(view)
            self.m_hsplit.show()

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
            index=self.m_hsplit.indexOf(currentView)
            index+=increment
            if index>=self.m_hlayout.count():
                index=0
            elif index<0:
                index=self.m_hlayout.count()-1
            view=self.m_hsplit.widget(index)
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
                view=self.m_hsplit.widget(index)
                self.setCurrentView(view)
                self.focusCurrentView()

    def open(self, document, how='reset', focus=True):

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

    def currentView(self):

        return self.view

    def setCurrentView(self, view):

        if view!=self.view: 
            self.view=view
            self.viewChanged.emit(self.view)

    def deactivate(self, focusView=True):

        if self.activated:
            self.activated=False
            statusbar=self.app.window.statusBar()
            statusbar.details.setText('')
            statusbar.hide()
            if focusView: self.focusCurrentView()

    def toggle(self):

        statusbar=self.app.window.statusBar()
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

    @register(key='s', modes=['command'])
    def saveDocument(self): 

        if self.view: self.view.save()

    @register(key='vC', modes=['command'])
    def closeCurrentView(self): self.closeView(self.currentView())

    @register(key='vd', modes=['command', 'normal'])
    def focusDown(self): self.focus(+1)

    @register(key='vu', modes=['command', 'normal'])
    def focusUp(self): self.focus(-1)

    @register(key='vc', modes=['command', 'normal'])
    def focusCurrentView(self):

        self.deactivate(focusView=False)
        self.setFocus()
        if self.view: self.view.setFocus()
