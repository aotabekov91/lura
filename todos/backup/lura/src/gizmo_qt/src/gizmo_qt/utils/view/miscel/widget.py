from PyQt6 import QtCore, QtWidgets

from gizmo_qt import vimo


class WidgetView(vimo.View, QtWidgets.QWidget):
    def setup(self):
        super().setup()
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowFlags(
            QtCore.Qt.WindowType.FramelessWindowHint
        )
        self.setAttribute(
            QtCore.Qt.WidgetAttribute.WA_TranslucentBackground
        )
