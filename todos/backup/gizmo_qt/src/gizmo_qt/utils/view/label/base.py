from PyQt6 import QtWidgets
from gizmo_qt.vimo import view


class LabelView(
    view.View,
    QtWidgets.QLabel,
):
    pass
