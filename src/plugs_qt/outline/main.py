from plug import Plug, tag

from .view import OutlineView

class Outline(Plug):

    section_ratios={0: .75, 1: .25}

    def setup(self):
        super().setup()
        self.m_outliners={}
        self.setupView()

    # todo
    #     self.app.main.display.viewChanged.connect(self.on_viewChanged)
    #     self.app.main.display.itemChanged.connect(self.on_viewItemChanged)

    def updateHeaderRatio(self):
        header=self.view.header()
        width=self.view.size().width()
        for i, v in self.section_ratios.items():
            header.resizeSection(
                    i, int(width*v))

    def setupView(self):
        self.view=self.app.buffman.createView(
                OutlineView, None)
        self.app.stateman.viewChanged.connect(
                self.updateOutline)
        self.view.resized.connect(
                self.updateHeaderRatio)

    def addOutliner(self, name, outliner):
        self.m_outliners[name]=outliner

    def outliner(self, name):
        return self.m_outliners.get(name, None)

    def updateOutline(self, view):
        model=view.model()
        name=model.__class__.__name__
        outliner=self.outliner(name)
        if outliner:
            outline=outliner.getOutline(model)
            if outline:
                self.view.setModel(outline)

    @tag('<c-o>(normal/outline)')
    def toggleOutline(self):
        self.view.toggle()

    @tag('o(normal)[OutlineView]')
    def open(self, view=None, focus=False):
        item=self.view.currentItem()
        goer=self.app.plugman.plugs.get('Go')
        if not view:
            view=self.app.stateman.subview()
        if item and goer:
            data=item.data()
            goer.goTo(view=view, **data)
            if focus:
                view.activate()

    @tag('O(normal)[OutlineView]')
    def openAndFocus(self, *args, **kwargs):
        kwargs['focus']=True
        self.open(*args, **kwargs)
