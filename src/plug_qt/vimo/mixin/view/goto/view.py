from PyQt6 import QtCore, QtWidgets

from .base import Go


class ViewGo(Go):
    def goTo(self, xrange=None, **kwargs):
        if xrange is None:
            self.goToLast()
        else:
            idx = self.getRowIndex(xrange[-1] - 1)
            self.setCurrentIndex(idx)

    def goToFirst(self, **kwargs):
        self.goTo(xrange=[1])

    def goToLast(self, **kwargs):
        m = self.m_model
        if self.checkProp("rowCount", m):
            xrange = [m.rowCount()]
        else:
            xrange = [m.count()]
        self.goTo(xrange)

    def goToUp(self, xrange=[1], **kwargs):
        for row in range(xrange[-1]):
            self.move("MoveUp")

    def goToDown(self, xrange=[1], **kwargs):
        for row in range(xrange[-1]):
            self.move("MoveDown")

    def move(self, arg):
        action = getattr(
                QtWidgets.QAbstractItemView.CursorAction, 
                arg, 
                None)
        if not action is None:
            item = self.moveCursor(
                action,
                QtCore.Qt.KeyboardModifier.NoModifier,
            )
            self.setCurrentIndex(item)
            self.scrollTo(item, QtWidgets.QAbstractItemView.ScrollHint.PositionAtCenter)
        else:
            self.goToFirst()

    def getRowIndex(self, row):
        return self.model().index(row, 0)

    def setCurrentIndex(self, idx):
        super().setCurrentIndex(idx)
        if type(idx) == int:
            self.indexChanged.emit(idx)
        else:
            self.indexChanged.emit(idx.row() + 1)
