import plug_qt
from PyQt6 import QtWidgets

from . import mixin


class FitzItem(
    mixin.Links,
    plug_qt.mixin.item.Scale,
    plug_qt.mixin.item.Select,
    plug_qt.mixin.item.Overlay,
    plug_qt.mixin.item.Annotate,
    plug_qt.mixin.item.Highlight,
    plug_qt.mixin.item.Render,
    plug_qt.vimo.item.Item,
    QtWidgets.QGraphicsObject,
):
    pass
