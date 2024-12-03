from gizmo.ui.qt.vimo import view
from gizmo.utils import tag

from .proxy import Dirs

class DirsView(
        view.FilterListView
        ):
    
    def setup(self):

        super().setup()
        m=Dirs(app=self.app)
        self.setModel(m)

    @tag('<c-h>', modes=['input|^'])
    def rootUp(self): 

        self.m_model.rootUp()
        text=self.app.view.bar.text()
        self.m_model.setFilter(text)

    @tag('<c-l>', modes=['input|^'])
    def rootDown(self):

        idx=self.currentIndex()
        self.m_model.rootDown(idx)
        text=self.app.view.bar.text()
        self.m_model.setFilter(text)

    def handleOpen(self, idx, *args, **kwargs):

        p=self.m_model.fullpath(idx)
        self.octivate()
        self.parent().octivate()
        self.app.buffman.open(
                p, recursive_activate=True)

    def setModel(self, *args, **kwargs):

        super().setModel(*args, **kwargs)
        if self.m_model:
            self.m_model.rootChanged.connect(
                    self.resetModel)

    def resetModel(self, *args, **kwargs):

        self.goToFirst()
        self.updatePosition()
        self.modelChanged.emit(self.m_model)

    def setupFilterOnActivate(self, *args, **kwargs):

        if not self.m_model.rootPath():
            self.m_model.setRootPath('.')
        self.app.view.bar.textChanged.connect(
                self.updateFilter)

    def setupFilterOnDeactivate(self, *args, **kwargs):

        self.app.view.bar.textChanged.disconnect(
                self.updateFilter)
        self.m_model.setFilter()
