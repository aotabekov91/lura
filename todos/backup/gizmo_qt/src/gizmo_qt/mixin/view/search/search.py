from PyQt6 import QtCore

from gizmo.utils import tag

from .task import SearchTask


class Search:
    canSearch = True
    searchFound = QtCore.pyqtSignal()

    def setup(self):
        super().setup()
        self.m_search_idx = -1
        self.m_search_data = []
        self.m_search_match = None
        self.setupSearchTask()
        self.searchFound.connect(self.updateSearchInfo)

    def setupSearchTask(self, task=SearchTask):
        t = task()
        self.m_search_task = t
        self.clearSearchData()
        t.signals.ready.connect(self.updateSearchData)
        self.app.pool.start(t)

    @tag("j(search[jump])[^]")
    def next(self, xrange=[1]):
        self.go(
            kind="next",
            xrange=xrange,
            mode="search",
        )

    @tag("k(search[jump])[^]")
    def prev(self, xrange=[1]):
        self.go(
            kind="prev",
            xrange=xrange,
            mode="search",
        )

    @tag("gg(search[jump])[^]")
    def first(self, xrange=[1]):
        self.go(
            kind="first",
            xrange=xrange,
            mode="search",
        )

    @tag("G(search[jump])[^]")
    def searchGoTo(
        self,
        kind=None,
        xrange=None,
        **kwargs,
    ):
        d = self.m_search_data
        idx = self.m_search_idx
        if not d:
            return
        if kind == "first":
            idx = 0
        elif kind == "last":
            idx = len(d) - 1
        elif kind == "next":
            idx += 1
        elif kind == "prev":
            idx -= 1
        elif xrange is None:
            idx = len(d) - 1
        else:
            idx = xrange[-1] - 1
        if idx >= len(d):
            idx = 0
        elif idx < 0:
            idx = len(d) - 1
        self.searchSetCurrentIndex(idx)
        return idx

    @tag("{/}(normal)[^]")
    def toggleSearchMode(self, **kwargs):
        mode = self.app.stateman.toggle(
            mode="search", passive=["search"]
        )
        if mode:
            self.activateSearchBar()
        else:
            self.updateSearchInfo(clear=True)

    @tag("{/}(search[jump])[^]")
    def activateSearchBar(self):
        self.updateSearchInfo(True)
        self.app.stateman.setSubmode()
        self.app.view.bar.activateEdit("/", keep=True)

    @tag("<c-[>/<escape>(search[any])[^]")
    def octivateSearchMode(self):
        self.updateSearchInfo(clear=True)
        self.app.view.bar.octivateEdit()
        self.app.stateman.toggle()
        self.clearSearchData()

    @tag("<return>(search)[^]")
    def startSearch(self):
        self.setFocus()
        self.app.stateman.setSubmode("jump")
        t = self.app.view.bar.text()
        self.clearSearchData()
        self.search(t)

    def searchCount(self):
        return len(self.m_search_data)

    def searchCurrentIndex(self):
        return self.m_search_idx

    def search(self, text):
        self.m_search_task.start(text, self)

    def clearSearchData(self):
        self.m_search_idx = -1
        self.m_search_data = []
        self.m_search_match = None
        self.m_search_task.start()

    def updateSearchData(self, data):
        self.m_search_data += data
        self.searchFound.emit()
        if self.m_search_idx < 0:
            self.next()

    def updateSearchInfo(self, clear=False):
        d = None
        if not clear:
            c = self.searchCount()
            i = self.searchCurrentIndex()
            d = f"{i+1}/{c}"
        self.app.view.bar.setInfo(d)

    def searchSetCurrentIndex(self, idx):
        self.m_search_idx = idx
        self.updateSearchInfo()

    def searchGetItem(self, idx):
        if idx < len(self.m_search_data):
            return self.m_search_data[idx]
