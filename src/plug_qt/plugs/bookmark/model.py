from PyQt6 import QtCore

from plug import Element
from plug_qt import vimo

class BookmarkElement(Element, QtCore.QObject):
    pass

class BookmarkModel(vimo.Model, QtCore.QObject):

    element_class=BookmarkElement

    def add(self, data):
        position = data.get("position")
        element = self.get(position)
        if not element:
            element=self.createElement(data)
        else:
            self.updateElement(element, data)
        return element

    def remove(self, element=None, data=None, by='position'):
        if not element and data:
            position = data.get(by)
            element = self.get(position)
        return self.delElement(element)

    def get(self, bmark, by="position"):
        return self.getElement(bmark, by=by)
