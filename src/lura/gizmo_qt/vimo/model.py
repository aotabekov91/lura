from PyQt6 import QtCore

from lura.gizmo.ui.core import vimo


class Model(vimo.Model):
    loaded = QtCore.pyqtSignal(object)
    idChanged = QtCore.pyqtSignal(object)
    elementAdded = QtCore.pyqtSignal(object)
    elementWanted = QtCore.pyqtSignal(object)
    elementRemoved = QtCore.pyqtSignal(object)
    elementUpdated = QtCore.pyqtSignal(object)
    elementCreated = QtCore.pyqtSignal(object)
    modelAdded = QtCore.pyqtSignal(object, object)
