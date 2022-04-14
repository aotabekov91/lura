from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.core.buffer import BufferManager
from lura.core.plugin import PluginManager
from lura.core.widgets import DisplaySplitter

class WindowManager(QMainWindow):

    continuousModeChanged = pyqtSignal(bool, object)
    documentModified = pyqtSignal(object)
    currentPageChanged = pyqtSignal(object, int, object)
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
        self.setStyleSheet("background-color: white;")

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
        self.display.focusMapView()

    def focusDocumentView(self):
        self.display.focusDocumentView()

    def focusBrowserView(self):
        self.display.focusBrowserView()

    def onlyMapView(self):
        self.display.onlyMapView()

    def onlyDocumentView(self):
        self.display.onlyDocumentView()

    def onlyBrowserView(self):
        self.display.onlyBrowserView()

    def createDisplay(self):

        self.display=DisplaySplitter()
        self.setCentralWidget(self.display)

    def resetView(self, m_view):

        self.display.setWidget(m_view)

        if self.m_view is not None: self.m_view.save()

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

        locs = {
                'left': Qt.LeftDockWidgetArea,
                'bottom': Qt.BottomDockWidgetArea,
                'top': Qt.TopDockWidgetArea,
                'right': Qt.RightDockWidgetArea,
                }

        for name, loc in locs.items():

            dockWidget = QDockWidget(self)
            dockWidget.setStyleSheet("background-color: white;")
            # dockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)

            stackWidget= QStackedWidget(self)
            stackWidget.setStyleSheet("background-color: white;")

            dockWidget.setWidget(stackWidget)

            self.addDockWidget(loc, dockWidget)

            setattr(self, '{}Stack'.format(name), stackWidget)
            setattr(self, '{}Dock'.format(name), dockWidget)

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

        # self.buffer.updateViews()
        # self.m_view.updateSceneAndView()
        # self.m_view.setFocus()

    def deactivateTabWidget(self, widget):

        widget.m_dockWidget.hide()
        widget.m_tabWidget.hide()
        widget.hide()

        # self.buffer.updateViews()
        # self.m_view.updateSceneAndView()
        # self.m_view.setFocus()

    def activateTabWidget(self, widget):

        widget.m_dockWidget.setTitleBarWidget(widget.m_qlabel)
        widget.m_tabWidget.setCurrentIndex(widget.m_tabIndex)
        widget.m_dockWidget.show()
        widget.m_tabWidget.show()
        widget.show()

        # self.buffer.updateViews()
        # self.m_view.updateSceneAndView()
    
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

    def close(self):
        if self.m_view is not None: self.m_view.save()
        super().close()

    def save(self):
        if self.m_view is not None: self.m_view.save()

