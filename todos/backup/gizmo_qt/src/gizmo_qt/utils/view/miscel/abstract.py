from PyQt6 import QtWidgets

from gizmo_qt import vimo


class AbstractView(
    vimo.View,
    QtWidgets.QWidget,
):
    pass
