from PyQt6 import QtCore, QtWidgets

import plug_qt

from .item import FitzItem
from .utils import Viewport

class FitzView(
    plug_qt.vimo.mixin.view.Scene,
    plug_qt.vimo.mixin.view.Scale,   #todo: should be factored out
    plug_qt.vimo.mixin.view.ZXYPos,  #todo: should be factored out
    plug_qt.vimo.mixin.view.Locate,  #todo: should be factored out
    plug_qt.vimo.mixin.view.SceneGo, #todo: should be factored out
    plug_qt.vimo.view.View,
    QtWidgets.QGraphicsView,
):
    hasItems = True
    canFollow = True
    canUpdateItems = True
    indexChanged = QtCore.pyqtSignal(object)
    itemPainted = QtCore.pyqtSignal(
        object, object, object, object)

    item_class = FitzItem
    position = {"FitzView": "C|x"}

    def setup(self):
        self.m_curr = 1
        self.m_items = {}
        self.m_prev = None
        self.m_fetched = -1
        self.m_viewport = Viewport()
        self.setViewport(self.m_viewport)
        self.m_viewport.updated.connect(self.updateItems)
        super().setup()

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

    def updateItems(self):
        if self.m_fetched >= self.count():
            self.m_viewport.updated.disconnect(self.updateItems)
        else:
            r = self.viewport().geometry()
            r = self.mapToScene(r)
            self.addItemsNear(r.boundingRect())

    def setItems(self, model):
        x = self.logicalDpiX()
        y = self.logicalDpiY()
        elems = model.elements().values()
        for j, e in enumerate(elems):
            i = self.createItem(j, e)
            i.setVisible(False)
            i.setResol(x, y)
            self.m_items[e.index()] = i
        self.redraw()

    def redraw(self):
        self.viewIsToBeRedrawn.emit()
        self.updateLayout()
        self.viewport().update()
        super().redraw()

    def createItem(self, idx, element):
        item=self.item_class(
            view=self,
            element=element,
            index=idx + 1,
            scaleFactor=self.scaleFactor,
            config=self.m_config.get("Item", {}),
            convertToGrayScale=self.convertToGrayScale)
        item.painted.connect(self.itemPainted)
        return item

    def setCurrentIndex(self, idx):
        if self.m_curr != idx:
            c, p = idx, self.m_curr
            self.m_curr, self.m_prev = c, p
        self.indexChanged.emit(self.m_curr)

    def refresh(self):
        for j, i in self.getItems():
            i.refresh(dropCache=True)

    def updateCurrent(self, refresh=False):
        i = self.currentItem()
        i.refresh(dropCache=refresh)

    def updateVisibile(self, refresh=False):
        for i in self.m_items.values():
            if i.isVisible():
                i.refresh(refresh)

    def visibleItems(self):
        r = self.viewport().rect()
        return self.items(r)

    def setVisibleItem(self):
        v = self.viewport()
        v.update()
        r = self.viewport().rect()
        x, w = int(r.width() / 2 - 5), 10
        y, h = int(r.height() / 2 - 5), 10
        v = QtCore.QRect(x, y, w, h)
        i = self.items(v)
        idx = self.m_curr
        if i:
            idx = i[0].index()
        self.setCurrentIndex(idx)

    def item(self, idx=None, element=None):
        if element:
            for i in self.m_items.values():
                if i.element() == element:
                    return i
        else:
            return self.m_items.get(idx, None)

    def getItems(self):
        return self.m_items.items()

    def count(self):
        if self.m_model:
            return self.m_model.count()
        return len(self.m_items)

    def currentItem(self):
        return self.item(self.m_curr)

    def currentIndex(self):
        return self.m_curr

    def addItemsNear(self, rect):
        for idx, i in self.m_items.items():
            c1 = i.scene()
            c2 = i.isVisible()
            if c1 and c2:
                continue
            else:
                if not rect.intersects(i.m_rect):
                    continue
                if not c1:
                    self.m_fetched += 1
                    self.m_scene.addItem(i)
                if not c2:
                    i.setVisible(True)
