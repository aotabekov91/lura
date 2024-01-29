from gizmo import mixin
from PyQt5.QtWidgets import QAbstractItemView

class Go(mixin.view.ViewGo):
    
    def go(self, *args, **kwargs):

        super().go(*args, **kwargs)
        self.update()

    def goTo(self, rstart=None, **kwargs):

        path=kwargs.get('path')
        if type(rstart)==int:
            pidx=self.currentIndex().parent()
            idx=self.m_model.index(rstart-1, 0, pidx)
            self.setCurrentIndex(idx)
        elif path:
            idx=self.m_model.index(path)
            self.setRootIndex(idx.parent())
            self.setCurrentIndex(idx)
        else:
            super().goTo(rstart=rstart, **kwargs)

    def goToLast(self, **kwargs):

        pidx=self.currentIndex().parent()
        rcount=self.m_model.rowCount(pidx)
        idx=self.m_model.index(rcount-1, 0, pidx)
        self.setCurrentIndex(idx)

    def goToFirst(self, **kwargs):

        pidx=self.currentIndex().parent()
        idx=self.m_model.index(0, 0, pidx)
        self.setCurrentIndex(idx)

    def goToRight(self, rstart=1, **kwargs):
        
        for i in range(rstart):
            idx=self.currentIndex()
            if self.m_model.isDir(idx):
                c=self.m_model.index(0, 0, idx)
                self.setRootIndex(idx)
                self.setCurrentIndex(c)

    def goToLeft(self, rstart=1, **kwargs):

        for i in range(rstart):
            r=self.rootIndex()
            p=r.parent()
            if p: 
                self.setRootIndex(p)
                self.setCurrentIndex(r)

    def setCurrentIndex(self, idx):

        super().setCurrentIndex(idx)
        p=idx.parent()
        path=self.m_model.filePath(p)
        self.m_model.setId(path)
        self.modelChanged.emit(self.m_model)
        self.scrollTo(
                idx, QAbstractItemView.PositionAtCenter)

    def setRootIndex(self, idx):

        super().setRootIndex(idx)
        if self.m_model.canFetchMore(idx):
            self.m_model.fetchMore(idx)
        rc=self.m_model.rowCount(idx)
        for i in range(rc):
            c=self.m_model.index(i, 0, idx)
            p=self.m_model.filePath(c)
            i=self.m_model.index(p)
            if self.m_model.canFetchMore(i):
                self.m_model.fetchMore(i)
