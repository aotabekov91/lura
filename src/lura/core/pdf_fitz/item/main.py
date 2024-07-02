import gizmo_qt
from PyQt6 import QtWidgets

from . import mixin


class FitzItem(
    mixin.Links,
    gizmo_qt.mixin.item.Scale,
    gizmo_qt.mixin.item.Select,
    gizmo_qt.mixin.item.Overlay,
    gizmo_qt.mixin.item.Annotate,
    gizmo_qt.mixin.item.Highlight,
    gizmo_qt.mixin.item.Render,
    gizmo_qt.vimo.item.Item,
    QtWidgets.QGraphicsObject,
):
    pass
