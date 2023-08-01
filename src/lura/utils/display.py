from PyQt5 import QtCore

from qapp.app import Display

class LuraDisplay(Display):

    annotationAdded=QtCore.pyqtSignal(object)
    annotationCreated=QtCore.pyqtSignal(object)
    annotationRegistered=QtCore.pyqtSignal(object)
