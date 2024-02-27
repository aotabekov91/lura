from gizmo.ui.qt.mixin import view
from PyQt5 import QtCore

from .task import SearchTask


class Search(view.Search):
    def setupSearchTask(self, task=SearchTask):
        super().setupSearchTask(SearchTask)

    def searchSetCurrentIndex(self, idx):
        d = self.m_search_data
        i, r = d[idx]
        if self.checkProp("canHighlight", i):
            i.highlight({"box": [r]})
        d = i.index()
        x, y = r.x(), r.y()
        self.goTo(d, x, y)
        pos = self.getBarPosition(d, x, y)
        if pos:
            c = QtCore.QPointF(*pos)
            self.centerOn(c)
        super().searchSetCurrentIndex(idx)

    def clearSearchData(self):
        self.cleanUp()
        self.cleanUpSearch()
        super().clearSearchData()

    def cleanUpSearch(self):
        if not self.m_search_data:
            return
        for i, r in self.m_search_data:
            if self.checkProp("canHighlight", i):
                i.highlight()
