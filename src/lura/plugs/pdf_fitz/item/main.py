import gizmo
from PyQt5 import QtWidgets

from . import mixin

class FitzItem(
        mixin.Links,
        gizmo.qt.mixin.item.Scale, 
        gizmo.qt.mixin.item.Select,
        gizmo.qt.mixin.item.Overlay,
        gizmo.qt.mixin.item.Annotate,
        gizmo.qt.mixin.item.Highlight, 
        gizmo.qt.mixin.item.Render, 
        gizmo.qt.vimo.item.Item,
        QtWidgets.QGraphicsObject,
        ):
    pass
