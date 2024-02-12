from gizmo import mixin
from PyQt5 import QtCore 
from gizmo.vimo import item, view

class DirItem(mixin.view.Scene):

    hasItems=True
    canUpdateItems=True
    item_class=item.Item

    def setup(self):

        super().setup()
        self.indexChanged.connect(
                self.reindexModel)

    def visibleItems(self):
        return [self.m_item]

    def createItem(self):

        x=self.logicalDpiX()
        y=self.logicalDpiY()
        config=self.m_config.get('Item', {})
        self.m_item=self.item_class(
                view=self,
                config=config,
                scaleFactor=self.scaleFactor,
                )
        self.m_scene.addItem(self.m_item)
        self.m_item.setResol(x, y)
        self.m_item.setVisible(True)

    def setModel(self, model):

        self.clearScene()
        if id(self.m_model)!=id(model):
            self.m_curr=None
            self.m_prev=None
            self.createItem()
            self.modelIsToBeChanged.emit(
                    self, self.m_model)
            self.m_model=model
            self.kind=model.kind
            self.setElement()
            self.modelLoaded.emit(
                    self, self.m_model)
            self.modelChanged.emit(
                    self.m_model)

    def setElement(self):

        e=self.m_model.createElement()
        self.m_elem=e
        self.m_item.setElement(e)
        self.item(1)
        self.redraw()

    def redraw(self):

        self.viewIsToBeRedrawn.emit()
        self.updateLayout()
        super().redraw()

    def updateLayout(self):

        r=self.m_item.boundingRect()
        self.m_scene.setSceneRect(r)
        self.setSceneRect(r)

    def setCurrentIndex(self, idx):

        if self.m_curr!=idx:
            c, p = idx, self.m_curr
            self.m_curr, self.m_prev=c, p
            self.m_elem.resetIndex(idx)
            self.indexChanged.emit(self.m_curr)

    def refresh(self):
        self.m_item.refresh(dropCache=True)

    def updateCurrent(self, refresh=False):
        self.m_item.refresh(dropCache=refresh)

    def updateVisibile(self, refresh=False):
        self.updateCurrent(refresh)

    def item(self, idx=None):

        self.setCurrentIndex(idx)
        self.updateLayout()
        return self.m_item

    def count(self):
        return self.m_model.count()

    def currentItem(self):
        return self.m_item

    def currentIndex(self):
        return self.m_curr

    def setVisibleItem(self):

        self.centerOn(self.m_item)
        # return

    def reindexModel(self, idx):

        e=self.m_item.element()
        if not e: return
        self.m_model.setId(e.identifier())
        self.modelChanged.emit(self.m_model)

    def getItems(self):

        idx=self.m_item.index()
        return [(idx, self.m_item)]
