from PyQt6 import QtCore

import plug


class Item(plug.Item):
    viewIsSet = QtCore.pyqtSignal()
    elementIsSet = QtCore.pyqtSignal()

    def setElement(self, element):
        super().setElement(element)
        if element:
            self.elementIsSet.emit()

    def setView(self, view):
        super().setView(view)
        if view:
            self.viewIsSet.emit()
