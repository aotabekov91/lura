from PyQt6 import QtCore

from ..base import Model
from .task import SortFilterTask


class SortFilterProxyModel(
    Model, QtCore.QSortFilterProxyModel
):
    filter_thread = True
    populated = QtCore.pyqtSignal(int)
    scoreUpdated = QtCore.pyqtSignal()
    filterChanged = QtCore.pyqtSignal()

    def setup(self):
        super().setup()
        self.setTimer()
        self.setSource()
        self.m_filter_cache = {}
        self.m_filter_text = None
        self.setFilterSortTask()

    def setFilterSortTask(self, task=SortFilterTask):
        if self.filter_thread:
            d = QtCore.QThread()
            t = task(self.m_source)
            self.m_regex_task = t
            self.m_regex_thread = d
            t.ready.connect(self.saveScore)
            d.started.connect(t.run)
            t.moveToThread(d)
            d.start()

    def saveScore(self, rid, alist):
        d = self.m_filter_cache[rid]
        for p, s in alist:
            d[p] = s
        if self.m_filter_text == rid:
            self.invalidate()

    def score(self, idx, kind=None, fidx=None):
        if not self.m_filter_text:
            return 1
        fidx = fidx or self.m_filter_text
        if not fidx:
            return 1
        if fidx in self.m_filter_cache:
            p = self.m_source.data(idx)
            d = self.m_filter_cache.get(fidx)
            return d.get(p, -1)
        else:
            self.m_filter_cache[fidx] = {}
            self.m_regex_task.start(fidx)
            return -1

    def lessThan(self, l, r):
        if self.m_filter_text:
            ls = self.score(l, kind="score")
            rs = self.score(r, kind="score")
            return ls < rs
        return False

    def filterAcceptsRow(self, r, p):
        if self.m_filter_text:
            idx = self.m_source.index(r, 0, p)
            p = self.m_source.data(idx)
            return self.score(idx, kind="filter") > 0
        return True

    def setTimer(self):
        t = QtCore.QTimer()
        t.timeout.connect(self.resetFilter)
        self.m_timer = t

    def setFilter(self, fltr=""):
        self.m_timer.stop()
        self.m_filter_text = fltr
        self.m_timer.start(500)

    def resetFilter(self):
        self.m_timer.stop()
        self.invalidate()
        self.resetSort()
        self.scoreUpdated.emit()

    def setSource(self, m=None):
        if m:
            self.m_source = m
            self.setSourceModel(m)
            m.populated.connect(self.populated)

    def count(self):
        return self.rowCount()

    def resetSort(self):
        pass
