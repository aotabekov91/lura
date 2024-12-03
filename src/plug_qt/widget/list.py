from PyQt6 import QtCore, QtWidgets

class ListViewWidget(QtWidgets.QListView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def currentItem(self, idx=None):
        model = self.model()
        if model:
            idx = idx or self.currentIndex()
            if type(model) == QtCore.QSortFilterProxyModel:
                idx = model.mapToSource(idx)
            if hasattr(model, "itemFromIndex"):
                return model.itemFromIndex(idx)
