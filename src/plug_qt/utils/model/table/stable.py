from PyQt6.QtGui import QStandardItemModel

from plug_qt.mixin.item import StandardItem

from .base import TableModel


class STableModel(QStandardItemModel, TableModel):
    item_class = StandardItem

    def createElement(self, idx, data):
        e = super().createElement(idx, data)
        self.createItem(e)
        return e

    def addElement(self, data):
        e = super().addElement(data)
        self.createItem(e)
        return e

    def createItem(self, e):
        i = e.item()
        if not i:
            i = self.item_class()
            e.setItem(i)
            self.appendRow(i)
        return i

    def removeElement(self, e):
        super().removeElement(e)
        row = e.item().index().row()
        self.removeRow(row)
        return e
