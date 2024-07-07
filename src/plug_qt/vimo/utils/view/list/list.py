from plug_qt import vimo
from plug_qt.vimo.mixin import view
from plug_qt.widget import ListViewWidget


class ListView(
    view.ViewGo,
    vimo.View,
    ListViewWidget,
):
    def setModel(self, model):
        if model:
            super().setModel(model)
            super(ListViewWidget, self).setModel(model)
