from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import watch, Configure

from .viewer import View

class Display(QWidget):

    keyPressEventOccurred=pyqtSignal(object)

    viewCreated=pyqtSignal(object)
    viewChanged=pyqtSignal(object)

    annotationAdded=pyqtSignal(object)
    annotationCreated=pyqtSignal(object)
    annotationRegistered=pyqtSignal(object)

    currentPageChanged = pyqtSignal(object, int)

    mouseDoubleClickOccured = pyqtSignal(object, object, object)
    mouseReleaseEventOccured = pyqtSignal(object, object, object)
    mouseMoveEventOccured = pyqtSignal(object, object, object)
    mousePressEventOccured = pyqtSignal(object, object, object)
    hoverMoveEventOccured = pyqtSignal(object, object, object)

    pageItemHasBeenJustCreated = pyqtSignal(object, object)
    pageHasBeenJustPainted = pyqtSignal(object, object, object, object, object)

    def __init__(self, app):
        super().__init__()

        self.app=app
        self.count=-1
        self.m_view=None
        self.activated=False
        self.views={}

        # self.style_sheet='''
        #     QWidget {
        #         background-color: green
        #         }
        #     separator {
        #         color: red;
        #         width: 5px; 
        #         height: 0px; 
        #         margin: 0px; 
        #         padding: 0px; 
        #         }
        #         '''
        # self.setStyleSheet(self.style_sheet)

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

    def setActions(self):
        self.configure=Configure(self.app, 'Display', self)

    def clear(self):
        for index in range(self.m_hlayout.count(),-1, -1):
            item=self.m_hlayout.takeAt(index)
            if item: item.widget().hide()
        self.m_hsplit.hide()

    def setView(self, view, how=None, focus=True):
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

    @watch(widget='own', context=Qt.WidgetShortcut)
    def focusDown(self):
        self.focus(+1)

    @watch(widget='own', context=Qt.WidgetShortcut)
    def focusUp(self):
        self.focus(-1)

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

    @watch(widget='own', context=Qt.WidgetShortcut)
    def closeCurrentView(self):
        self.closeView(self.currentView())

    def open(self, document, how='reset', focus=True):
        self.m_view=self.createView(document)
        self.m_view.show()
        self.m_view.readjust()
        self.m_view.fitToPageWidth()
        self.m_view.setFocus()

        self.m_view.annotationAdded.connect(self.annotationAdded)

        self.setView(self.m_view, how, focus)
        self.viewChanged.emit(self.m_view)

    def createView(self, document):
        view=View(self.app)
        self.count+=1
        view.setId(self.count)
        self.views[self.count]=view
        view.open(document)
        self.viewCreated.emit(view)
        return view

    def currentView(self):
        return self.m_view

    def setCurrentView(self, view):
        self.m_view=view
        self.viewChanged.emit(self.m_view)

    @watch(widget='own', context=Qt.WidgetShortcut)
    def focusCurrentView(self):
        self.deactivate(focusView=False)
        view=self.currentView()
        if view:
            view.setFocus()
        else:
            self.setFocus()

    def deactivate(self, focusView=True):
        if self.activated:
            self.activated=False
            statusbar=self.app.window.statusBar()
            statusbar.setDetailInfo('')
            statusbar.hide()
            if focusView: self.focusCurrentView()

    @watch(widget='window', context=Qt.WindowShortcut)
    def toggle(self):
        statusbar=self.app.window.statusBar()
        if not self.activated:
            self.activated=True
            statusbar.setDetailInfo(self.configure.name)
            statusbar.show()
            self.show()
            self.setFocus()
        else:
            self.deactivate()

    def keyPressEvent(self, event):
        self.keyPressEventOccurred.emit(event)
        super().keyPressEvent(event)
