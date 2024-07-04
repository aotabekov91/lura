from gizmo_qt import vimo
from gizmo_qt.mixin import view
from gizmo_qt.widget import ListViewWidget


class ListView(
    view.ViewGo,
    vimo.View,
    ListViewWidget,
):
    def setModel(self, model):
        if model:
            super().setModel(model)
            super(ListViewWidget, self).setModel(model)
