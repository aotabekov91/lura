from PyQt6 import QtCore, QtWidgets


class Viewport(QtWidgets.QWidget):
    updated = QtCore.pyqtSignal()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.updated.emit()

    def event(self, e):
        res = super().event(e)
        if e.type() == QtCore.QEvent.Type.Move:
            self.update()
        return res
