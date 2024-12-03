from PyQt6 import QtCore, QtWidgets

class TreeViewWidget(QtWidgets.QTreeView):

    itemChanged = QtCore.pyqtSignal(object)
    indexChanged = QtCore.pyqtSignal(object)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setHeaderHidden(True)
        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def expand(self, idx=None, **kwargs):
        idx = idx or self.currentIndex()
        self.setCurrentIndex(idx)
        super().expand(idx)

    def expandAll(self, idx=None, **kwargs):
        if idx is None:
            super().expandAll()
        elif idx.isValid():
            if not self.isExpanded(idx):
                self.expand(idx)
            for row in range(self.model().rowCount()):
                self.expandAll(idx.child(row, 0))

    def expandAbove(self, child, **kwargs):
        index = child.parent()
        while index.isValid():
            index = index.parent()
            self.expand(index)

    def collapseAll(self, idx=None, **kwargs):
        if idx is not None and idx.isValid():
            if not self.isExpanded(idx):
                self.collapse(idx)
            for row in range(self.model().rowCount()):
                self.collapseAll(idx.child(row, 0))
        else:
            super().collapseAll()

    def collapseAllInside(self, item=None, **kwargs):
        item = item or self.currentItem()
        if item:
            super().collapse(item.index())
            for i in range(item.rowCount()):
                self.collapseAllInside(item.child(i))

    def collapse(self, idx=None, **kwargs):
        idx = idx or self.currentIndex()
        super().collapse(idx)

    def rootDown(self, xrange=[1], **kwargs):
        for d in range(xrange):
            idx = self.currentIndex()
            if idx:
                self.setRootIndex(idx)
                child = idx.child(0, 0)
                self.setCurrentIndex(child)

    def rootUp(self, xrange=[1], **kwargs):
        for d in range(xrange):
            idx = self.rootIndex()
            p = idx.parent()
            if p.isValid():
                self.setRootIndex(p)
                self.setCurrentIndex(idx)

    def parentUp(self, xrange=[1], **kwargs):
        for i in range(xrange):
            idx = self.currentIndex()
            p = idx.parent()
            if p.isValid():
                self.setCurrentIndex(p)
            else:
                f = self.m_model.index(0, 0)
                return self.setCurrentIndex(f)

    def siblingDown(self, xrange=[1], **kwargs):
        for row in range(xrange):
            self.goToSibling(kind="down")

    def siblingUp(self, xrange=[1], **kwargs):
        for row in range(xrange):
            self.goToSibling(kind="up")

    def goToSibling(self, kind="up", **kwargs):
        idx = self.currentIndex()
        if not idx:
            return
        s_idx = idx.row() + 1
        if kind == "up":
            s_idx = idx.row() - 1
        elif kind == "down":
            s_idx = idx.row() + 1
        p = idx.parent()
        if p.isValid():
            n_idx = p.child(s_idx, 0)
        else:
            n_idx = self.m_model.index(s_idx, 0)
        self.setCurrentIndex(n_idx)

    def first(self, **kwargs):
        kwargs['xrange']=[1]
        self.goTo(**kwargs)

    # def last(self):
    #     idx = self.rootIndex()
    #     if idx:
    #         m = self.model()
    #         lr = m.rowCount(idx) - 1
    #         last = idx.child(lr, 0)
    #         self.setCurrentIndex(last)

    def last(self, **kwargs):
        index = self.currentIndex()
        if index:
            parent = index.parent()
            last_row = index.model().rowCount(parent) - 1
            last = self.m_model.index(last_row, 0, parent)
            self.setCurrentIndex(last)

    def goToLast(self, **kwargs):
        m = self.m_model
        if self.checkProp("rowCount", m):
            xrange = [m.rowCount()]
        else:
            xrange = [m.count()]
        self.goTo(xrange)


    def right(self, **kwargs):
        self.expand()

    def left(self, **kwargs):
        self.collapse()

    def up(self, xrange=[1], **kwargs):
        for row in range(xrange[-1]):
            self.move("MoveUp")

    def down(self, xrange=[1], **kwargs):
        for row in range(xrange[-1]):
            self.move("MoveDown")

    def firstSibling(self, **kwargs):
        idx = self.currentIndex()
        if idx:
            p = idx.parent()
            f = p.child(0, 0)
            self.setCurrentIndex(f)

    def lastSibling(self, **kwags):
        index = self.currentIndex()
        if index:
            parent = index.parent()
            last_row = index.model().rowCount(parent) - 1
            last = parent.child(last_row, 0)
            self.setCurrentIndex(last)

    def goTo(self, kind=None, xrange=None, **kwargs):
        if kind:
            func=getattr(self, kind, None)
            if func:
                func(xrange=xrange, **kwargs)
        elif xrange:
            idx = self.getRowIndex(xrange[-1])
            self.setCurrentIndex(idx)
        elif xrange is None:
            self.last(xrange=xrange, **kwargs)

    def move(self, arg, **kwargs):
        cursor=QtWidgets.QAbstractItemView.CursorAction
        action = getattr(cursor, arg, None)
        if not action is None:
            mode=QtCore.Qt.KeyboardModifier.NoModifier
            hint=QtWidgets.QAbstractItemView.ScrollHint
            ensure=hint.EnsureVisible
            idx = self.moveCursor(action, mode)
            self.setCurrentIndex(idx)
            self.scrollTo(idx, ensure) 

    # def getRowIndex(self, row):
    #     idx = self.model().index(0, 0)
    #     for i in range(row):
    #         idx = self.indexBelow(idx)
    #     return idx

    # todo: go to last
    def getRowIndex(self, row):
        idx = self.currentIndex()
        pidx = idx.parent()
        return pidx.child(row, 0)

    def setCurrentIndex(self, idx):
        if idx is None:
            return
        if not idx.isValid():
            return
        if self.model() is None:
            return
        super().setCurrentIndex(idx)
        if self.currentItem() is None:
            return
        self.indexChanged.emit(idx)
        self.itemChanged.emit(self.currentItem())
        self.selectionModel().select(
            idx,
            QtCore.QItemSelectionModel.SelectionFlag.Current,
        )
        if hasattr(self.model(), "itemChanged"):
            self.model().itemChanged.emit(
                self.currentItem()
            )

    def currentItem(self, idx=None):
        m = self.model()
        if m:
            idx = idx or self.currentIndex()
            if type(m) == QtCore.QSortFilterProxyModel:
                idx = m.mapToSource(idx)
            if idx and hasattr(m, "itemFromIndex"):
                return m.itemFromIndex(idx)
