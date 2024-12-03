from gizmo_qt import vimo, widget


class TreeView(
    vimo.View,
    widget.TreeViewWidget,
):
    def setModel(self, model):
        if model:
            self.m_model
            super().setModel(model)
            super(widget.TreeViewWidget, self).setModel(
                model
            )
