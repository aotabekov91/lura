import plug_qt
from PyQt6 import QtWidgets

class FitzItem(
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
