from gizmo import mixin

from .task import SearchTask

class Search(mixin.view.Search):

    def setupSearchTask(
            self, task=SearchTask):

        super().setupSearchTask(SearchTask)

    def searchSetCurrentIndex(self, idx):

        d=self.m_search_data
        i, r = d[idx]
        if self.checkProp('canHighlight', i):
            i.highlight({'box': [r]})
        d = i.index()
        x, y = r.x(), r.y()-0.45
        self.goTo(d, x, y)
        super().searchSetCurrentIndex(idx)

    def clearSearchData(self):

        super().clearSearchData()
        self.cleanUpSearch()

    def cleanUpSearch(self):

        for (i, r) in self.m_search_data:
            if self.checkProp('canHighlight', i):
                i.highlight()
