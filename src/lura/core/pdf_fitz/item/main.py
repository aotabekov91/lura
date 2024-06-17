from lura import qt
from PyQt6 import QtWidgets

from . import mixin


class FitzItem(
    mixin.Links,
    qt.mixin.item.Scale,
    qt.mixin.item.Select,
    qt.mixin.item.Overlay,
    qt.mixin.item.Annotate,
    qt.mixin.item.Highlight,
    qt.mixin.item.Render,
    qt.vimo.item.Item,
    QtWidgets.QGraphicsObject,
):
    pass
