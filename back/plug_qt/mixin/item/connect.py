from PyQt6 import QtCore


class Connect:
    canConnect = True
    mouseReleaseOccured = QtCore.pyqtSignal(object, object)
    mouseMoveOccured = QtCore.pyqtSignal(object, object)
    mousePressOccured = QtCore.pyqtSignal(object, object)
    hoverMoveOccured = QtCore.pyqtSignal(object, object)
    mouseDoubleClickOccured = QtCore.pyqtSignal(
        object, object
    )

    def mouseDoubleClickEvent(self, e):
        self.mouseDoubleClickOccured.emit(self, e)

    def mousePressEvent(self, e):
        self.mousePressOccured.emit(self, e)

    def mouseMoveEvent(self, e):
        self.mouseMoveOccured.emit(self, e)

    def mouseReleaseEvent(self, e):
        self.mouseReleaseOccured.emit(self, e)

    def hoverMoveEvent(self, e):
        self.hoverMoveOccured.emit(self, e)
