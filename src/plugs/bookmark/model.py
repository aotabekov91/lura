from PyQt6 import QtCore

from plug import Element
from plug_qt import vimo

class BookmarkElement(Element, QtCore.QObject):
    pass

class BookmarkModel(vimo.Model, QtCore.QObject):

    element_class=BookmarkElement

    def addBookmark(self, data):
        position = data.get("position")
        element = self.getBookmark(position)
        if not element:
            element=self.createElement(data)
        else:
            self.updateElement(element, data)
        return element

    def getBookmark(self, bmark, by="position"):
        return self.getElement(bmark, by=by)

    def delBookmark(self, element=None, data=None):
        if not element and data:
            position = data.get("position")
            element = self.getBookmark(position)
        return self.delElement(element)
