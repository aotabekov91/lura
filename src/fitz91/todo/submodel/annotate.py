from PyQt6 import QtCore

from plug import Element
from plug_qt.vimo import Model
from plug.utils import Factory


class Annotate:
    canAnnotate = True

    def setup(self):
        super().setup()
        mklass = Factory(Model, QtCore.QObject)
        eklass = Factory(Element, QtCore.QObject)
        self.m_annotations = mklass(
            name="annotation",
            element_class=eklass,
        )
        self.addModel("annotation", self.m_annotations)

    def addAnnotation(self, data):
        idx = data.get("id")
        e = self.getAnnotation(idx)
        if not e:
            self.m_annotations.createElement(data)
        else:
            self.m_annotations.updateElement(e, data)

    def getAnnotation(self, idx, by="id"):
        return self.m_annotations.getElement(idx, by=by)

    def delAnnotation(self, data):
        idx = data.get("id")
        e = self.getAnnotation(idx)
        self.m_annotations.delElement(e)
