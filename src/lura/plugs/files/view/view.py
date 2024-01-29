import gizmo

from . import mixin

class FilesView(
        mixin.Go,
        mixin.Copy,
        mixin.Line,
        mixin.Search,
        mixin.Visual,
        mixin.PLocate,
        mixin.OLocate,
        gizmo.mixin.view.Bookmark,
        gizmo.mixin.view.Quickmark,
        gizmo.mixin.view.Fullscreen,
        gizmo.vimo.view.ListView,
        ):

    canFollow=True
    default_mode='normal'
    prefix_keys={'|^own': '<c-.>'}
    position={'FilesView': '!FilesTab'}

    def count(self):

        if self.m_model:
            idx=self.currentIndex()
            pidx=idx.parent()
            return self.m_model.rowCount(pidx)

    def setPath(self, path=None):

        m=self.m_model
        idx=m.getPathIndex(path)
        self.setRootIndex(idx)

    def setSource(self, source):

        m=self.m_model
        idx=m.getPathIndex(source)
        self.setRootIndex(idx.parent())
        self.expand(idx)

    def resetConfigure(
            self, 
            model=None, 
            **kwargs):

        if model:
            s=model.source()
            idx=model.index(s)
            p=idx.parent()
            self.setRootIndex(p)
            self.setCurrentIndex(idx)
