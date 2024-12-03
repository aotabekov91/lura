from PyQt6 import QtCore, QtGui

from ..list import ListView


class OverlayList(ListView):
    def __init__(
        self,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.setModel()

    def setModel(self):
        self.m_model = QtGui.QStandardItemModel()
        super().setModel(self.m_model)

    def updateData(self, alist=[]):
        self.m_model.clear()
        if alist:
            for t in alist:
                i = QtGui.QStandardItem(t)
                self.m_model.appendRow(i)
            self.updatePosition()
        else:
            self.hide()

    def show(self):
        if self.m_model.rowCount() > 0:
            super().show()

    def sizeHint(self):
        w = self.width()
        n = self.m_model.rowCount()
        if n == 0:
            return QtCore.QSize(w, 0)
        c = 0
        h = self.sizeHintForRow(0)
        for i in range(n):
            ih = self.sizeHintForColumn(i)
            c = max(c, ih)
        c += 10
        r = self.parent().rect()
        dy = self.rect().y()
        w = min(int(0.8 * r.width() - dy), c)
        h = min(int(0.9 * r.height()), h * n)
        return QtCore.QSize(w, h)

    def updatePosition(
        self, gx=None, gy=None, gw=None, gh=None
    ):
        p = self.parent().rect()
        if p:
            self.adjustSize()
            w, h = self.width(), self.height()
            y = int(p.height() / 2 - self.height() / 2)
        gx = gx or 0
        gy = gy or y
        gw = gw or w
        gh = gh or h
        self.setGeometry(gx, gy, gw, gh)
