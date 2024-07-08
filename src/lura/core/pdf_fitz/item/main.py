import plug_qt
from PyQt6 import QtWidgets

from . import mixin


class FitzItem(
    # mixin.Links,
    plug_qt.vimo.mixin.item.Scale,
    plug_qt.vimo.mixin.item.Select,
    plug_qt.vimo.mixin.item.Overlay,
    plug_qt.vimo.mixin.item.Annotate,
    plug_qt.vimo.mixin.item.Highlight,
    plug_qt.vimo.mixin.item.Render,
    plug_qt.vimo.item.Item,
    QtWidgets.QGraphicsObject,
):
    pass
