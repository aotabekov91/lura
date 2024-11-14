import plug_qt
from PyQt6 import QtWidgets

class FitzItem(
    plug_qt.vimo.mixin.item.Overlay,
    plug_qt.vimo.mixin.item.Render,
    plug_qt.vimo.item.Item,
    QtWidgets.QGraphicsObject,
):
    pass
