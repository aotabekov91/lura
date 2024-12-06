from PyQt6 import QtCore, QtWidgets, QtGui

from plug_qt import vimo, gizmo

from .item import FitzItem
from .utils import Viewport, FitzScene

class FitzView(
    vimo.View,
    QtWidgets.QGraphicsView,
):
    canFollow = True
    scene_color = "black"
    position = {"FitzView": "C|x"}
    indexChanged = QtCore.pyqtSignal(object)
    pixmapReady = QtCore.pyqtSignal(object, object, object)
    itemPainted = QtCore.pyqtSignal(object, object, object, object)

    def setup(self):
        self.m_items = {}
        self.m_current = 1
        self.m_fetched = -1
        self.m_scene = None
        self.m_previous = None
        self.m_viewport = Viewport()
        self.m_norm = QtGui.QTransform()
        self.setViewport(self.m_viewport)
        self.m_viewport.updated.connect(self.updateItems)
        self.setupScene()
        self.setupLayout()
        super().setup()

    def setLayout(self, layout):
        self.m_layout = layout
        self.redraw()

    def layout(self):
        return self.m_layout

    def refreshItem(self, idx, data, pixmap):
        item=self.item(idx)
        if item and item.keys()==data:
            item.refresh()

    def setupScene(self):
        scene = FitzScene() 
        self.m_scene = scene
        self.setScene(scene)
        if self.scene_color:
            color = QtGui.QColor(self.scene_color)
            scene.setBackgroundBrush(color)

    def setupLayout(self):
        config = self.m_config.get("Layout", {})
        self.m_layout = gizmo.Layout(
            self, config=config)

    def clearScene(self):
        self.m_scene.clear()

    def setModel(self, model):
        self.clearScene()
        if id(self.m_model) != id(model):
            self.m_items = {}
            self.m_fetched = 0
            self.modelIsToBeChanged.emit(self, self.m_model)
            self.m_model = model
            self.kind = model.kind
            self.setItems(model)
            model.modelUpdated.connect(self.redraw)
            self.modelLoaded.emit(self, self.m_model)
            self.modelChanged.emit(self.m_model)
            model.pixmapReady.connect(self.refreshItem)

    def updateItems(self):
        if self.m_fetched >= self.count():
            self.m_viewport.updated.disconnect(self.updateItems)
        else:
            viewport = self.viewport()
            rect = viewport.geometry()
            rect = self.mapToScene(rect)
            self.addItemsNear(rect.boundingRect())

    def setItems(self, model):
        x = self.logicalDpiX()
        y = self.logicalDpiY()
        elems = model.elements().values()
        for idx, elem in enumerate(elems):
            item = self.createItem(idx, elem)
            item.setVisible(False)
            item.setResol(x, y)
            self.m_items[elem.index()] = item
        self.redraw()

    def redraw(self):
        self.viewIsToBeRedrawn.emit()
        self.app.buffman.viewIsToBeDrawn.emit(self)
        position=self.getScenePosition()
        self.updateLayout()
        self.setScenePosition(position)
        self.viewport().update()
        super().redraw()
        self.app.buffman.viewIsDrawn.emit(self)

    def updateLayout(self):
        y = 0.0
        x, r, h = self.m_layout.load(self.m_items)
        w = r - x
        self.m_scene.setSceneRect(x, y, w, h)
        self.setSceneRect(QtCore.QRectF(x, y, w, h))
        self.updateNormTransform()

    def updateNormTransform(self):
        self.m_norm.reset()
        rect=self.sceneRect()
        size=rect.size()
        self.m_norm.scale(size.width(), size.height())

    def getScenePosition(self):
        view=self.viewport().rect()
        scene=self.mapToScene(view).boundingRect()
        inv=self.m_norm.inverted()[0]
        position=inv.map(scene.center())
        return position

    def setScenePosition(self, position):
        position=self.m_norm.map(position)
        self.centerOn(position)

    def createItem(self, idx, element):
        item=FitzItem(
            view=self,
            element=element,
            index=idx + 1,
            scaleFactor=self.scaleFactor,
            config=self.m_config.get("Item", {}),
            convertToGrayScale=self.convertToGrayScale)
        item.painted.connect(self.itemPainted)
        return item

    def currentIndex(self):
        return self.m_current

    def setCurrentIndex(self, idx):
        if self.m_current != idx:
            current, previous = idx, self.m_current
            self.m_current, self.m_previous = current, previous
        self.indexChanged.emit(self.m_current)

    def refresh(self):
        for idx, item in self.getItems():
            item.refresh(dropCache=True)

    def updateCurrent(self, refresh=False):
        item = self.currentItem()
        item.refresh(dropCache=refresh)

    def updateVisibile(self, refresh=False):
        for item in self.m_items.values():
            if item.isVisible():
                item.refresh(refresh)

    def visibleItems(self):
        rect = self.viewport().rect()
        return self.items(rect)

    def setVisibleItem(self):
        viewport = self.viewport()
        viewport.update()
        r = self.viewport().rect()
        x, w = int(r.width() / 2 - 5), 10
        y, h = int(r.height() / 2 - 5), 10
        viewport = QtCore.QRect(x, y, w, h)
        item = self.items(viewport)
        idx = self.m_current
        if item:
            idx = item[0].index()
        self.setCurrentIndex(idx)

    def item(self, idx=None, element=None):
        if element:
            for item in self.m_items.values():
                if item.element() == element:
                    return item
        else:
            return self.m_items.get(idx, None)

    def getItems(self):
        return self.m_items.items()

    def count(self):
        if self.m_model:
            return self.m_model.count()
        return len(self.m_items)

    def currentItem(self):
        return self.item(self.m_current)

    def addItemsNear(self, rect):
        for idx, item in self.m_items.items():
            cond1 = item.scene()
            cond2 = item.isVisible()
            if cond1 and cond2:
                continue
            else:
                if not rect.intersects(item.m_rect):
                    continue
                if not cond1:
                    self.m_fetched += 1
                    self.m_scene.addItem(item)
                if not cond2:
                    item.setVisible(True)
