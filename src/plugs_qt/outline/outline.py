from plug import Plug, tag

from .view import OutlineView

class Outline(Plug):

    def setup(self):

        super().setup()
        self.setupView()

    def view(self):
        return self.view

    def setupView(self):
        self.view=self.app.buffman.createView(
                OutlineView, None)
        self.connectView()

    def connectView(self):
        self.app.stateman.viewChanged.connect(
                self.updateOutline)

    def updateOutline(self, view):
        
        model=view.model()
        manager=view.manager()
        if view==self.view:
            return
        if not model:
            return
        if not self.app.check('hasOutline', model):
            return
        central_view=False
        while manager:
            if manager==self.app.ui.main:
                central_view=True
                break
            manager=manager.manager()
        outline=model.outline()
        self.view.setModel(outline)

    @tag('<c-o>(normal/outline)')
    def toggleOutline(self):
        self.view.toggle()
