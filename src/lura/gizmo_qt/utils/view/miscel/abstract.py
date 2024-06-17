from PyQt6 import QtWidgets

from lura.qt import vimo


class AbstractView(
    vimo.View,
    QtWidgets.QWidget,
):
    pass
