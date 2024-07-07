from PyQt6 import QtWidgets

from plug_qt import vimo


class AbstractView(
    vimo.View,
    QtWidgets.QWidget,
):
    pass
