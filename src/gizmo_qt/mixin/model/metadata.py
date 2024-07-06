from PyQt6 import QtCore

from gizmo import Element, Model
from app.utils import Factory


class Metadata:
    hasMetadata = True

    def setup(self):
        super().setup()
        mklass = Factory(Model, QtCore.QObject)
        eklass = Factory(Element, QtCore.QObject)
        self.m_metadata = mklass(
            name="metadata", element_class=eklass
        )
        self.addModel("metadata", self.m_metadata)

    def addMetadata(self, data):
        f = data.get("field")
        e = self.getMetadata(f, by="field")
        data[f] = data.get("value")
        if not e:
            self.m_metadata.addElement(data)
        else:
            self.m_metadata.updateElement(e, data)

    def getMetadata(self, idx, by="hash"):
        return self.m_metadata.getElement(idx, by=by)

    def delMetadata(self, data):
        m = data.get("hash")
        e = self.getMetadata(m)
        self.m_metadata.delElement(e)
