from PyQt6 import QtCore

from plug import Element
from plug_qt import vimo

class AnnotateElement(Element, QtCore.QObject):
    pass

class AnnotateModel(vimo.Model, QtCore.QObject):

    element_class=AnnotateElement

    def addAnnotate(self, data):
        position = data.get("position")
        element = self.getAnnotate(position)
        if not element:
            element=self.createElement(data)
        else:
            self.updateElement(element, data)
        return element

    def getAnnotate(self, bmark, by="position"):
        return self.getElement(bmark, by=by)

    def delAnnotate(self, element=None, data=None):
        if not element and data:
            position = data.get("position")
            element = self.getAnnotate(position)
        return self.delElement(element)
