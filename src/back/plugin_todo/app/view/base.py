from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..scene import Scene
from ..plugin import Configure

class View(QGraphicsView):

    resized=pyqtSignal(object, object)

    modelModified = pyqtSignal(object)
    layoutModeChanged = pyqtSignal(object)

    itemChanged = pyqtSignal(object, object)
    itemPainted = pyqtSignal(object, object, object, object, object)

    keyPressOccurred=pyqtSignal([object, object])

    hoverMoveOccured = pyqtSignal([object, object])
    mouseMoveOccured = pyqtSignal([object, object])
    mousePressOccured = pyqtSignal([object, object])
    mouseReleaseOccured = pyqtSignal([object, object])
    mouseDoubleClickOccured = pyqtSignal([object, object])

    itemHoverMoveOccured = pyqtSignal([object, object, object])
    itemMouseMoveOccured = pyqtSignal([object, object, object])
    itemMousePressOccured = pyqtSignal([object, object, object])
    itemMouseReleaseOccured = pyqtSignal([object, object, object])
    itemMouseDoubleClickOccured = pyqtSignal([object, object, object])

    def __init__(self, app, layout, scene_class=None):

        super().__init__(app.main)

        self.app=app
        self.m_model=None
        self.m_id=id(self)
        self.m_selected=[]

        self.zoom=1
        self.zoomInFactor=1.25
        self.zoomOutFactor=0.75
        self.zoomRange=[-10, 10]

        self.configure=Configure(app, 'View', self)
        self.s_settings=self.configure.getSettings()

        self.setup(scene_class, layout)
        self.connect()

    def setup(self, scene_class, layout):

        if not scene_class: scene_class=Scene

        self.m_scene=scene_class()
        self.m_scene.itemAdded.connect(self.on_itemAdded)

        self.setScene(self.m_scene)
        self.m_layout = layout(self)
        self.scene().setBackgroundBrush(QColor('black'))

        self.setAcceptDrops(False)
        self.setDragMode(QGraphicsView.ScrollHandDrag)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def setId(self, vid): self.m_id=vid

    def id(self): return self.m_id

    def setLayout(self, layout):

        self.m_layout=layout
        self.layoutModeChanged.emit(self)

    def selected(self): return self.m_selected

    def deselect(self, item=None): self.m_selected=[]

    def select(self, selections=[]): 

        if self.m_selected: self.deselect(self.m_selected)
        self.m_selected=selections

    def show(self):

        super().show()
        self.readjust()
        self.setFocus()

    def connect(self):

        self.mouseDoubleClickOccured.connect(
                self.app.main.display.viewMouseDoubleClickOccured)
        self.mouseReleaseOccured.connect(
                self.app.main.display.viewMouseReleaseOccured)
        self.mouseMoveOccured.connect(
                self.app.main.display.viewMouseMoveOccured)
        self.mousePressOccured.connect(
                self.app.main.display.viewMousePressOccured)
        self.hoverMoveOccured.connect(
                self.app.main.display.viewHoverMoveOccured)

        self.itemMouseDoubleClickOccured.connect(
                self.app.main.display.itemMouseDoubleClickOccured)
        self.itemMouseReleaseOccured.connect(
                self.app.main.display.itemMouseReleaseOccured)
        self.itemMouseMoveOccured.connect(
                self.app.main.display.itemMouseMoveOccured)
        self.itemMousePressOccured.connect(
                self.app.main.display.itemMousePressOccured)
        self.itemHoverMoveOccured.connect(
                self.app.main.display.itemHoverMoveOccured)

        self.itemChanged.connect(
                self.app.main.display.itemChanged)
        self.itemPainted.connect(
                self.app.main.display.itemPainted)

    def resizeEvent(self, event):

        super().resizeEvent(event)
        self.resized.emit(self, event)
        self.readjust()

    def mouseMoveEvent(self, event):
        
        super().mouseMoveEvent(event)
        self.mouseMoveOccured.emit(self, event)

    def mousePressEvent(self, event):

        super().mousePressEvent(event)
        self.mousePressOccured.emit(self, event)

    def mouseReleaseEvent(self, event):
        
        super().mouseReleaseEvent(event)
        self.mouseReleaseOccured.emit(self, event)

    def mouseDoubleClickEvent(self, event):

        super().mouseDoubleClickEvent(event)
        self.mouseDoubleClickOccured.emit(self, event)

    def on_itemAdded(self, item):

        item.itemPainted.connect(
                self.on_itemPainted)
        item.mouseDoubleClickOccured.connect(
                self.on_itemMouseDoubleClickOccured)
        item.mousePressOccured.connect(
                self.on_itemMousePressOccured)
        item.mouseReleaseOccured.connect(
                self.on_itemMouseReleaseOccured)
        item.mouseMoveOccured.connect(
                self.on_itemMouseMoveOccured)
        item.hoverMoveOccured.connect(
                self.on_itemHoverMoveOccured)

    def on_itemPainted(self, painter, options, widget, page):
        self.itemPainted.emit(painter, options, widget, page, self)

    def on_itemMouseDoubleClickOccured(self, item, event):
        self.itemMouseDoubleClickOccured.emit(self, item, event)

    def on_itemMousePressOccured(self, item, event):
        self.itemMousePressOccured.emit(self, item, event)

    def on_itemMouseReleaseOccured(self, item, event):
        self.itemMouseReleaseOccured.emit(self, item, event)

    def on_itemMouseMoveOccured(self, item, event):
        self.itemMouseMoveOccured.emit(self, item, event)

    def on_itemHoverMoveOccured(self, item, event):
        self.itemHoverMoveOccured.emit(self, item, event)

    def readjust(self): pass

    def left(self): pass

    def right(self): pass

    def down(self): pass

    def up(self): pass

    def pageUp(self): pass

    def pageDown(self): pass
    
    def pageLeft(self): pass

    def pageRight(self): pass

    def incrementRight(self): pass

    def incrementLeft(self): pass

    def incrementUp(self): pass
    
    def incrementDown(self): pass

    def prev(self): pass

    def next(self): pass

    def goto(self, digit): pass

    def gotoEnd(self): pass

    def gotoBegin(self): pass

    def save(self): pass

    def cleanUp(self): pass

    def model(self): return self.m_model

    def setModel(self, model):

        self.scene().clear()
        self.m_model=model

    def zoomIn(self): self._zoom(kind='in')

    def zoomOut(self): self._zoom(kind='out')

    def _zoom(self, kind):

        if kind=='in':
            self.zoom += 1 
            if self.zoom <= self.zoomRange[1]:
                self.scale(self.zoomInFactor, self.zoomInFactor)
            else:
                self.zoom = self.zoomRange[1]
        elif kind=='out':
            self.zoom -= 1 
            if self.zoom >= self.zoomRange[0]:
                self.scale(self.zoomOutFactor, self.zoomOutFactor)
            else:
                self.zoom = self.zoomRange[0]

    def toggleCursor(self):

        if self.m_cursor==Qt.BlankCursor:
            self.m_cursor=Qt.ArrowCursor
        else:
            self.m_cursor=Qt.BlankCursor
        self.setCursor(self.m_cursor)

    def name(self): return id(self)

    def event(self, event):

        if event.type()==QEvent.Enter:
            self.setFocus()
            self.app.main.display.setCurrentView(self)
            self.app.modes.setMode('normal')
        return super().event(event)
