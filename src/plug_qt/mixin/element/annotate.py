from PyQt6 import QtCore


class Annotate:
    canAnnotate = True
    annotationAdded = QtCore.pyqtSignal(object)
    annotationRemoved = QtCore.pyqtSignal(object)
    annotationUpdated = QtCore.pyqtSignal(object)
