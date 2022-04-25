from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.core import BufferManager
from lura.core import PluginManager
from lura.core import DisplaySplitter

class WindowManager(QMainWindow):

    continuousModeChanged = pyqtSignal(bool, object)
    documentModified = pyqtSignal(object)
    currentPageChanged = pyqtSignal(object, int)
    layoutModeChanged = pyqtSignal(object, object)
    rubberBandModeChanged = pyqtSignal(str, object)
    scaleFactorChanged = pyqtSignal([float, object], [int, object])
    scaleModeChanged = pyqtSignal(str, object)
    rubberBandReady = pyqtSignal(
        object, 'QRectF', 'QRectF', object, object, object)
    mouseDoubleClickOccured = pyqtSignal(object, object, object)
    mouseReleaseEventOccured = pyqtSignal(object, object, object)
    mouseMoveEventOccured = pyqtSignal(object, object, object)
    mousePressEventOccured = pyqtSignal(object, object, object)
    hoverMoveEventOccured = pyqtSignal(object, object, object)
    pageItemHasBeenJustCreated = pyqtSignal(object, object)
    pageHasBeenJustPainted = pyqtSignal(object, object, object, object, object)

    titleChanged=pyqtSignal(object)
    documentTagged=pyqtSignal(int, str, object, object)

    mapItemChanged=pyqtSignal(QStandardItem)

    mapCreated=pyqtSignal(object)
    documentCreated=pyqtSignal(object)
    annotationCreated=pyqtSignal(object)
    noteCreated=pyqtSignal(object)

    documentRegistered=pyqtSignal(object)
    annotationRegistered=pyqtSignal(object)
    noteRegistered=pyqtSignal(object)

    viewChanged=pyqtSignal(object)

    def __init__(self, configuration):
        super().__init__()

        self.configuration=configuration
        self.createDocks()
        self.createDisplay()

        self.buffer=BufferManager(self, configuration)
        self.plugin=PluginManager(self, configuration)

        self.plugin.activatePlugins()

        self.setup()
        self.show()
        self.setFocus()

    def setup(self):

        # TODO: settings -> config.ini
        # self.settings=settings
        self.m_view=None
        stl="QWidget {color:white; background-color:black}; "
        stl+="separator {width: 0px; height: 0px; margin: 0px; padding: 0px; }"

        self.setStyleSheet(stl)

        self.setAcceptDrops(True)
        self.statusBar().setSizeGripEnabled(False)
        self.statusBar().hide()

        self.setActions()

    def setActions(self):

        self.m_actions=[]

        for func, key in self.configuration['Window']['shortcuts'].items():

            m_action=QAction(f'({key}) {func}')
            m_action.setShortcut(QKeySequence(key))
            m_action.setShortcutContext(Qt.ApplicationShortcut)
            self.m_actions+=[m_action]
            m_action.triggered.connect(getattr(self, func))
            self.addAction(m_action)

    def sizeHint(self):
        return QSize(1000, 1200)

    def focusMapView(self):
        view=self.display.focusMapView()
        self.setView(view)

    def isMapViewVisible(self):
        return self.display.isMapViewVisible()

    def focusDocumentView(self):
        view=self.display.focusDocumentView()
        self.setView(view)

    def isDocumentViewVisible(self):
        return self.display.isDocumentViewVisible()

    def onlyMapView(self):
        self.display.onlyMapView()

    def onlyDocumentView(self):
        self.display.onlyDocumentView()

    def toggleViews(self):
        if self.display.isVisible():
            self.display.hide()
        else:
            self.display.show()

    def createDisplay(self):

        self.display=DisplaySplitter()
        self.setCentralWidget(self.display)

    def closeView(self, filePath):
        view=self.buffer.close(filePath)
        if view is None: return
        if self.m_view==view: 
            self.m_view=None
        self.display.removeWidget(view)

    def resetView(self, m_view):

        self.display.setWidget(m_view)

        # if self.m_view is not None: self.m_view.save()

        self.m_view=m_view
        self.viewChanged.emit(m_view)

        m_view.show()
        m_view.readjust()
        m_view.fitToPageWidth()
        m_view.setFocus()

    def search(self, term):
        term='+'.join(term.split(' '))
        self.open(f'http://www.google.com/search?q={term}')

    def open(self, filePath=None, page=-1):

        m_view=self.buffer.open(filePath)
        if m_view is not None: self.resetView(m_view)

    def createDocks(self):

        self.state={}
        locs = {
                'left': Qt.LeftDockWidgetArea,
                'bottom': Qt.BottomDockWidgetArea,
                'top': Qt.TopDockWidgetArea,
                'right': Qt.RightDockWidgetArea,
                }

        for name, loc in locs.items():

            dockWidget = QDockWidget(self)
            stackWidget= MQStackedWidget(name, self)
            if name=='right':
                stackWidget.setFixedWidth(275)
            elif name=='left':
                stackWidget.setFixedWidth(450)
            else:
                stackWidget.setFixedHeight(275)
            dockWidget.setWidget(stackWidget)

            self.addDockWidget(loc, dockWidget)

            setattr(self, '{}Stack'.format(name), stackWidget)
            setattr(self, '{}Dock'.format(name), dockWidget)

        self.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)
        self.setCorner(Qt.BottomRightCorner, Qt.RightDockWidgetArea)

        self.hideAllDocks()

    def adjustTabWidgetSize(self):
        maxSize=QDesktopWidget().availableGeometry(self)
        width=maxSize.width()
        height=maxSize.height()
        for loc in ['left', 'bottom', 'top', 'right']:
            tab=getattr(self, '{}Tab'.format(loc))
            if loc in ['left', 'right']:
                tab.resize(width*0.2, height)
            else:
                tab.resize(width, height*0.2)

    def activateStatusBar(self, widget, stretch=1):

        self.statusBar().addWidget(widget, stretch)
        self.statusBar().show()
        widget.show()
        widget.setFocus()

    def deactivateStatusBar(self, widget):

        self.statusBar().removeWidget(widget)
        self.statusBar().hide()
        widget.hide()

    def focusLeft(self):
        if not self.leftDock.isVisible(): return
        if not self.leftDock in self.state: return
        if len(self.state[self.leftDock])==0: return
        index=self.state[self.leftDock][-1]
        self.leftStack.widget(index).setFocus()

    def focusUp(self):
        if not self.topDock.isVisible(): return
        if not self.topDock in self.state: return
        if len(self.state[self.topDock])==0: return
        index=self.state[self.topDock][-1]
        self.upStack.widget(index).setFocus()

    def focusBottom(self):
        if not self.bottomDock.isVisible(): return
        if not self.bottomDock in self.state: return
        if len(self.state[self.bottomDock])==0: return
        index=self.state[self.bottomDock][-1]
        self.bottomStack.widget(index).setFocus()

    def focusRight(self):
        if not self.rightDock.isVisible(): return
        if not self.rightDock in self.state: return
        if len(self.state[self.rightDock])==0: return
        index=self.state[self.rightDock][-1]
        self.rightStack.widget(index).setFocus()

    def deactivateTabWidget(self, widget):

        self.state[widget.m_dockWidget].pop(
                self.state[widget.m_dockWidget].index(widget.m_tabIndex))

        if len(self.state[widget.m_dockWidget])==0:
            widget.m_dockWidget.hide()
            widget.m_tabWidget.hide()
            widget.hide()
        else:
            oldWidgetIndex=self.state[widget.m_dockWidget][-1]
            widget.m_tabWidget.setCurrentIndex(oldWidgetIndex)

    def saveState(self, widget):
        if not widget.m_dockWidget in self.state:
            self.state[widget.m_dockWidget]=[]
        self.state[widget.m_dockWidget]+=[widget.m_tabIndex]

    def activateTabWidget(self, widget):

        self.saveState(widget)
        widget.m_dockWidget.setTitleBarWidget(widget.m_qlabel)
        widget.m_tabWidget.setCurrentIndex(widget.m_tabIndex)
        widget.m_dockWidget.show()
        widget.m_tabWidget.show()
        widget.show()

    def setTabLocation(self, widget, location, title):

        widget.m_tabWidget=getattr(self, '{}Stack'.format(location))
        widget.m_dockWidget=getattr(self, '{}Dock'.format(location))
        widget.m_tabIndex=widget.m_tabWidget.addWidget(widget)
        widget.m_qlabel=QLabel(title.title())

    def hideAllDocks(self, exclude=None):
        for dock in ['right', 'top', 'bottom', 'left']:
            dockWidget=getattr(self, f'{dock}Dock')
            if dockWidget!=exclude: 
                dockWidget.hide()

    def document(self):
        if self.m_view is not None:
            return self.m_view.document()

    def view(self):
        return self.m_view

    def setView(self, view):
        self.m_view=view
        self.viewChanged.emit(view)

    def close(self):
        if self.m_view is not None: self.m_view.save()
        super().close()

    def save(self):
        if self.m_view is not None: self.m_view.save()

class MQStackedWidget(QStackedWidget):

    def __init__(self, position, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.m_position=position
        self.setup()

    def setup(self):

        shortcut=QShortcut('+', self)
        shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        shortcut.activated.connect(self.increaseSize)

        shortcut=QShortcut('-', self)
        shortcut.setContext(Qt.WidgetWithChildrenShortcut)
        shortcut.activated.connect(self.decreaseSize)

    def increaseSize(self):
        s=self.size()
        w, h=s.width(), s.height()
        if self.m_position in ['left', 'right']:
            self.setFixedSize(round(w*1.2), h)
        else:
            self.setFixedSize(w, round(h*1.2))

    def decreaseSize(self):
        s=self.size()
        w, h=s.width(), s.height()
        if self.m_position in ['left', 'right']:
            self.setFixedSize(round(w*0.9), h)
        else:
            self.setFixedSize(w, round(h*0.9))
