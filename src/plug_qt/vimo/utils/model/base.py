from PyQt6 import QtCore

import plug

class Model(plug.Model):
    loaded = QtCore.pyqtSignal(object)
    idChanged = QtCore.pyqtSignal(object)
    elementAdded = QtCore.pyqtSignal(object)
    elementWanted = QtCore.pyqtSignal(object)
    elementRemoved = QtCore.pyqtSignal(object)
    elementUpdated = QtCore.pyqtSignal(object)
    elementCreated = QtCore.pyqtSignal(object)
    modelAdded = QtCore.pyqtSignal(object, object)
