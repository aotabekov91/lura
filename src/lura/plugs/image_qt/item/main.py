import gizmo
from PyQt5 import QtWidgets, QtCore

class ImageQtItem(
        gizmo.mixin.item.Scale,
        gizmo.mixin.item.Select,
        gizmo.mixin.item.Highlight, 
        gizmo.mixin.item.Render, 
        gizmo.vimo.item.Item, 
        QtWidgets.QGraphicsObject
        ):

    elementIsReset=QtCore.pyqtSignal()

    def setElement(self, elem):

        super().setElement(elem)
        if elem:
            elem.dataChanged.connect(
                    self.resetElement)

    def resetElement(self):

        idx=self.m_element.index()
        self.setIndex(idx)
        self.redraw()
        self.elementIsReset.emit()
