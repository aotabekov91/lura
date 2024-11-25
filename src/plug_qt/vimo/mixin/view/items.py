from PyQt6 import QtCore

from plug_qt.vimo.item import Item

from .scene import Scene
from .layout import Layout


class Items(Scene, Layout):
    hasItems = True
    item_class = Item

    def getItems(self):
        return self.m_items.items()

    def count(self):
        return len(self.m_items)

    def item(self, idx=None, element=None):
        if element:
            for i in self.m_items.values():
                if i.element() != element:
                    continue
                return i
        else:
            return self.m_items.get(idx, None)

    def setup(self):
        self.m_curr = 1
        self.m_items = {}
        self.m_prev = None
        super().setup()

    def setModel(self, model):
        self.clearScene()
        if model and id(self.m_model) != id(model):
            self.modelIsToBeChanged.emit(self, self.m_model)
            self.m_model = model
            self.kind = model.kind
            self.setItems(model)
            self.redraw()

    def setItems(self, model):
        self.m_items = {}
        c = self.m_config.get("Item", {})
        if self.item_class:
            elems = model.elements()
            for j, e in enumerate(elems.values()):
                i = self.item_class(
                    config=c,
                    index=j + 1,
                    element=e,
                    view=self,
                )
                self.setupItem(i)
        self.redraw()
        self.modelChanged.emit(model)
        self.modelLoaded.emit(self, model)

    def setupItem(self, i):
        idx = i.index()
        self.m_items[idx] = i
        x = self.logicalDpiX()
        y = self.logicalDpiY()
        i.setResol(x, y)
        self.m_scene.addItem(i)

    def redraw(self):
        self.redrawScene()
        self.redrawView()
        self.setVisibleItem()
        self.viewport().update()

    def redrawScene(self):
        h = self.m_layout.m_mode.pageSpacing
        l, r, h = self.m_layout.load(
            items=self.m_items, height=h
        )
        self.m_scene.setSceneRect(l, 0.0, r - l, h)

    def redrawView(self, *args, **kwargs):
        vv, hv = 0, 0
        s = self.m_scene
        r = s.sceneRect()
        l, t = r.left(), r.top()
        w, h = r.width(), r.height()
        for j, i in self.m_items.items():
            i.setVisible(True)
            pbr = i.boundingRect()
            pos = pbr.translated(i.pos())
            h += pos.height()
        self.setSceneRect(l, t, w, h)
        self.verticalScrollBar().setValue(vv)
        self.horizontalScrollBar().setValue(hv)
        self.viewport().update()

    def setCurrentIndex(self, idx):
        if self.m_curr != idx:
            c, p = idx, self.m_curr
            self.m_curr, self.m_prev = c, p
        c, p = self.m_curr, self.m_prev
        self.indexChanged.emit(c, p, self)

    def refresh(self):
        for j, i in self.getItems():
            i.refresh(dropCache=True)

    def currentItem(self):
        return self.item(self.m_curr)

    def currentIndex(self):
        return self.m_curr

    def updateCurrent(self, refresh=False):
        i = self.currentItem()
        i.refresh(dropCache=refresh)

    def updateVisibile(self, refresh=False):
        for i in self.m_items.values():
            if i.isVisible():
                i.refresh(refresh)

    def setVisibleItem(self):
        r = self.viewport().rect()
        x, w = int(r.width() / 2 - 5), 10
        y, h = int(r.height() / 2 - 5), 10
        v = QtCore.QRect(x, y, w, h)
        i = self.items(v)
        idx = self.m_curr
        if i:
            idx = i[0].index()
        self.setCurrentIndex(idx)

    def visibleItems(self):
        r = self.viewport().rect()
        return self.items(r)
