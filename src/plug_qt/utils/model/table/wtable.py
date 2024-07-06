from PyQt6 import QtCore

from plug_qt.mixin.item import ListWidgetItem
from plug_qt.widget import TableWidget

from .stable import STableModel


class WTableModel(STableModel):
    widget_map = {}
    widget_class = TableWidget
    list_item_class = ListWidgetItem
    widgetDataChanged = QtCore.pyqtSignal(object)

    def setup(self):
        super().setup()
        self.widgetDataChanged.connect(self.updateTableRow)

    def removeElement(self, e):
        super().removeElement(e)
        w = self.listWidget()
        if w:
            w.removeElement(e)

    def addElement(self, data):
        e = super().addElement(data)
        w = self.listWidget()
        if w:
            w.addElement(e)

    def createElement(self, idx, data):
        e = super().createElement(idx, data)
        self.createWidget(e)
        return self.createListItem(e)

    def createWidget(self, e):
        w = self.widget_class(
            element=e,
            wmap=self.widget_map,
            objectName="GridWidget",
        )
        e.setWidget(w)

    def createListItem(self, e):
        l = self.list_item_class()
        w = e.widget()
        w.setListItem(l)
        l.setElement(e)
        e.setListItem(l)
        return e

    @classmethod
    def isCompatible(cls, s, **kwargs):
        c = s and s == cls.pattern
        if not c:
            return
        c = kwargs.get("config", {})
        return c.get("widget_map", False)

    @classmethod
    def getSourceName(
        cls,
        source,
        name=None,
        index=None,
        **kwargs,
    ):
        return (index, name, source)
