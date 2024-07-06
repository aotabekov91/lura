from PyQt6 import QtCore

from gizmo import Element
from gizmo_qt.vimo import Model
from app.utils import Factory


class Bookmark:
    canBookmark = True

    def setup(self):
        super().setup()
        mklass = Factory(Model, QtCore.QObject)
        eklass = Factory(Element, QtCore.QObject)
        self.m_bookmarks = mklass(
            name="bookmark", element_class=eklass
        )
        self.addModel("bookmark", self.m_bookmarks)

    def addBookmark(self, data):
        pos = data.get("position")
        e = self.getBookmark(pos)
        if not e:
            self.m_bookmarks.createElement(data)
        else:
            self.m_bookmarks.updateElement(e, data)

    def getBookmark(self, bmark, by="position"):
        return self.m_bookmarks.getElement(bmark, by=by)

    def delBookmark(self, data):
        m = data.get("position")
        e = self.getBookmark(m)
        self.m_bookmarks.delElement(e)
