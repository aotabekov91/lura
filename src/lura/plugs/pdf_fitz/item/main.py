import gizmo
from PyQt6 import QtWidgets

from . import mixin


class FitzItem(
    mixin.Links,
    gizmo.ui.qt.mixin.item.Scale,
    gizmo.ui.qt.mixin.item.Select,
    gizmo.ui.qt.mixin.item.Overlay,
    gizmo.ui.qt.mixin.item.Annotate,
    gizmo.ui.qt.mixin.item.Highlight,
    gizmo.ui.qt.mixin.item.Render,
    gizmo.ui.qt.vimo.item.Item,
    QtWidgets.QGraphicsObject,
):
    pass
