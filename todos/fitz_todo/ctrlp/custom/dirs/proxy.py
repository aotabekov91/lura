import os
from PyQt5 import QtCore
from gizmo.ui.qt.vimo import model

from .source import SourceModel

class Dirs(
        model.SortFilterProxyModel
        ):

    isType=True
    rootChanged=QtCore.pyqtSignal()

    def setup(self):

        super().setup()
        self.m_root=None
        self.m_filter_index=(None, None)

    def setSource(self):

        super().setSource(
                SourceModel(app=self.app))

    def saveScore(
            self, 
            rid, 
            alist,
            ):

        super().saveScore(rid, alist)
        if self.m_filter_index==rid:
            self.beginResetModel()
            self.endResetModel()

    def setFilter(
            self, 
            fltr='',
            ):

        if not fltr: 
            self.m_source.setMinimumRowCount(100)
        self.m_filter_index=(self.m_root, fltr)
        super().setFilter(fltr)

    def score(
            self, 
            idx, 
            kind=None, 
            fidx=None
            ):

        return super().score(
                idx, 
                kind=kind, 
                fidx=self.m_filter_index)

    def resetSort(self):

        if self.m_filter_text:
            self.m_source.setMinimumRowCount()
            self.sort(0, QtCore.Qt.DescendingOrder)

    def rootUp(self):

        if self.m_root:
            path=self.m_root
            if path.endswith('/'):
                path=self.m_root[:-1]
            root='/'
            path=path.rsplit('/', 1)
            if path: root=path[0] 
            self.setRootPath(root)

    def rootDown(self, idx):

        idx=self.mapToSource(idx)
        path=self.m_source.data(idx)
        self.setRootPath(path)

    def setRootPath(self, path):

        if path:
            path=os.path.abspath(path)
            if not path.endswith('/'):
                path+='/'
            self.m_root=path
            self.m_source.setRootPath(path)
            self.setId(path)
            self.rootChanged.emit()

    def rootPath(self):
        return self.m_root

    def fullpath(self, idx):

        r=self.rootPath()
        cidx=self.mapToSource(idx)
        p=self.m_source.data(cidx)
        return os.path.join(r, p)
