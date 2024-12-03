from PyQt6 import QtCore, QtWidgets


class ListViewWidget(QtWidgets.QListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

    def currentItem(self, idx=None):
        m = self.model()
        if m:
            idx = idx or self.currentIndex()
            if type(m) == QtCore.QSortFilterProxyModel:
                idx = m.mapToSource(idx)
            if hasattr(m, "itemFromIndex"):
                return m.itemFromIndex(idx)
