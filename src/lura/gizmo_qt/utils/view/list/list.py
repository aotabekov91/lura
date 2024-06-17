from lura.qt import vimo
from lura.qt.mixin import view
from lura.qt.widget import ListViewWidget


class ListView(
    view.ViewGo,
    vimo.View,
    ListViewWidget,
):
    def setModel(self, model):
        if model:
            super().setModel(model)
            super(ListViewWidget, self).setModel(model)
