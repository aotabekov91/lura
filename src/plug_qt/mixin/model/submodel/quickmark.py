from PyQt6 import QtCore

from plug import Element
from plug_qt.vimo import Model
from plug.utils import Factory


class Quickmark:
    canQuickmark = True

    def setup(self):
        super().setup()
        mklass = Factory(Model, QtCore.QObject)
        eklass = Factory(Element, QtCore.QObject)
        self.m_quickmarks = mklass(
            name="quickmark",
            element_class=eklass,
        )
        self.addModel("quickmark", self.m_quickmarks)

    def addQuickmark(self, data):
        mark = data.get("mark")
        e = self.getQuickmark(mark)
        if not e:
            self.m_quickmarks.createElement(data)
        else:
            self.m_quickmarks.updateElement(e, data)

    def getQuickmark(self, mark, by="mark"):
        return self.m_quickmarks.getElement(mark, by=by)

    def delQuickmark(self, data):
        m = data.get("mark")
        e = self.getQuickmark(m)
        self.m_quickmarks.delElement(e)
