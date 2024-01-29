import os
from gizmo import mixin
from gizmo.utils import tag

class OLocate(mixin.view.Locate):

    @tag('o', modes=['|^own'])
    def open(self, **kwargs):

        m=self.m_model
        idx=self.currentIndex()
        path=m.filePath(idx)
        if m.isDir(idx):
            p=idx.parent()
            self.setRootIndex(p)
            self.setCurrentIndex(idx)
        else:
            self.app.ui.handler.open(
                    path, **kwargs)

    def openFile(
            self, 
            path=None, 
            how=None, 
            focus=False
            ):

        if not path:
            idx=self.ui.currentIndex()
            path=self.getPath(idx)
        if path:
            if os.path.isdir(path): 
                idx=self.ui.currentIndex()
                self.ui.expand(idx)
            else:
                self.app.open(
                        path, 
                        how=how, 
                        focus=focus)
                self.listen()
