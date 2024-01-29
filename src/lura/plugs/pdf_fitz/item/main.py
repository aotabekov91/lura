import gizmo
from PyQt5 import QtWidgets

from . import mixin

class FitzItem(
        mixin.Links,
        gizmo.mixin.item.Scale, 
        gizmo.mixin.item.Select,
        gizmo.mixin.item.Overlay,
        gizmo.mixin.item.Annotate,
        gizmo.mixin.item.Highlight, 
        gizmo.mixin.item.Render, 
        gizmo.vimo.item.Item,
        QtWidgets.QGraphicsObject,
        ):
    pass
