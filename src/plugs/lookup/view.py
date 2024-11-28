from plug_qt.vimo import mixin
from plug_qt.vimo.gizmo.view.tree import TreeView

class LookupView(
        mixin.view.TreeGo,
        TreeView
        ):

    position = {"LookupView": "D|D"}
