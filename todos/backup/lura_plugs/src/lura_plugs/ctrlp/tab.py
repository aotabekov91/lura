from gizmo.utils import tag
from gizmo.ui.qt.vimo import view

class CtrlPTab(view.TabView):

    position={'CtrlPTab': 'O'}

    @tag('<c-n>', modes=['input|^'])
    def gotoNext(self, *args, **kwargs):

        self.tabGoTo(kind='next')
        self.activate()

    @tag('<c-p>', modes=['input|^'])
    def gotoPrevious(self, *args, **kwargs):

        self.tabGoTo(kind='next')
        self.activate()

    @tag('<c-p>', modes=['normal'])
    def activate(self, **kwargs):

        super().activate(
                blur=False, 
                dark=False,
                **kwargs
                )
        self.app.stateman.setMode(
                'input', passive=['input'])
        self.app.view.bar.activateEdit('>')

    @tag(['<c-[>', '<escape>'], modes=['input|^'])
    def octivate(self, *args, **kwargs):

        self.app.view.bar.octivateEdit()
        super().octivate(*args, **kwargs)

    def sizeHint(self):

        if self.current:
            return self.current.sizeHint()
        return super().sizeHint()

    def updatePosition(self):

        w=self.app.view.size().width()
        uh=self.app.view.size().height()
        h=int(uh*0.4)
        if self.current:
            hint=self.current.sizeHint()
            h=min(h, hint.height())
        bh=self.app.view.bar.size().height()
        y=int(uh-h-bh)
        self.setGeometry(0, y, w, h)
