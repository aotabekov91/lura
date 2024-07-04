from PyQt6 import QtCore

from gizmo.utils import tag

from ..list import ListView


class FilterListView(ListView):
    openWanted = QtCore.pyqtSignal()

    @tag("<c-j>(input)[^]")
    def gotoNext(self):
        self.goToDown()

    @tag("<c-k>(input)[^]")
    def gotoPrev(self):
        self.goToUp()

    @tag("<c-J>(input)[^]")
    def gotoLast(self):
        self.goToLast()

    @tag("<c-K>(input)[^]")
    def gotoFirst(self):
        self.goToFirst()

    @tag("<c-m>(input)[^]")
    def open(self):
        idx = self.currentIndex()
        self.handleOpen(idx)

    @tag("<c-s>(input)[^]")
    def openSplitHorizontal(self):
        idx = self.currentIndex()
        self.handleOpen(idx, kind="horizontal")

    @tag("<c-v>(input)[^]")
    def openSplitVertical(self):
        idx = self.currentIndex()
        self.handleOpen(idx, kind="vertical")

    @tag("<c-t>(input)[^]")
    def openTab(self):
        idx = self.currentIndex()
        self.handleOpen(idx, kind="tab")

    def setModel(self, model, **kwargs):
        super().setModel(model, **kwargs)
        if self.m_model:
            m = self.m_model
            if hasattr(m, "scoreUpdated"):
                m.layoutChanged.connect(self.updatePosition)
                m.scoreUpdated.connect(self.updatePosition)

    def activate(self, *args, **kwargs):
        super().activate(*args, **kwargs)
        self.setupFilterOnActivate(*args, **kwargs)

    def octivate(self, *args, **kwargs):
        self.setupFilterOnDeactivate(*args, **kwargs)
        super().octivate(*args, **kwargs)

    def resetFilter(self):
        self.app.ui.bar.clearEdit()

    def updateFilter(self):
        if self.m_model:
            text = self.app.ui.bar.text()
            self.m_model.setFilter(text)

    def updatePosition(self, *args, **kwargs):
        p = self.parent()
        if p and self.checkProp("updatePosition", p):
            p.updatePosition()
        self.goToFirst()

    def filterSizeHint(self):
        h = super().sizeHint()
        if self.m_model.rowCount() > 0:
            c = self.m_model.rowCount()
            height = self.sizeHintForRow(0) * c
            h.setHeight(height + 5)
        return h

    def count(self):
        if self.m_model:
            return self.m_model.count()

    def sizeHint(self):
        return self.filterSizeHint()

    def handleOpen(self, *args, **kwargs):
        self.openWanted.emit()

    def setupFilterOnActivate(self, *args, **kwargs):
        pass

    def setupFilterOnDeactivate(self, *args, **kwargs):
        pass
