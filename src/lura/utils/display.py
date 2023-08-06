from PyQt5 import QtCore

from qapp.core.ui import Display as BaseDisplay

class Display(BaseDisplay):

    annotationAdded=QtCore.pyqtSignal(object)
    annotationCreated=QtCore.pyqtSignal(object)
    annotationRegistered=QtCore.pyqtSignal(object)
