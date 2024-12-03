from gizmo.plug import Plug 

from .tab import CtrlPTab
from .custom import DirsView
from .custom import FilesView

class CtrlP(Plug):

    name='ctrlp'

    def setup(self):

        super().setup()
        self.setupUI()
        self.setCustomViews()

    def setupUI(self):

        self.tab=CtrlPTab(app=self.app)
        self.app.buffman.locate(self.tab)

    def setCustomViews(self):

        v=DirsView(app=self.app)
        self.tab.addView(v)
        v=FilesView(app=self.app)
        self.tab.addView(v)
        self.tab.setView(v)
