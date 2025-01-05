from PyQt6 import QtCore

from plug import Plug, tag

from .view import OutlineView

class Outline(Plug):

    section_ratios={0: .75, 1: .25}

    def setup(self):
        super().setup()
        self.m_agents={}
        self.setupView()

    def addAgent(self, name, agent):
        self.m_agents[name]=agent

    def getAgent(self, name=None, view=None):
        if not name and view:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    def updateOutline(self, view):
        agent=self.getAgent(view=view)
        if agent:
            model=view.model()
            outline=agent.getOutline(model)
            if outline:
                self.m_view.setModel(outline)
                self.connectView(view)

    def connectView(self, view):
        if self.m_view:
            self.m_view.indexChanged.disconnect(
                    self.updateOutlineIndex)
        self.m_view=view
        view.indexChanged.connect(
                self.updateOutlineIndex)

    def updateOutlineIndex(self, idx):
        model=self.m_view.model()
        root_idx=QtCore.QModelIndex()
        found=self.find(idx, model, root_idx) 
        if found:
            self.m_view.setCurrentIndex(found)

    def find(self, idx, model, parent):
        for row in range(model.rowCount(parent)):
            title_idx=model.index(row, 0, parent)
            page_idx=model.index(row, 1, parent)
            page=int(page_idx.data())
            if idx==page: 
                return title_idx
        for row in range(model.rowCount(parent)):
            title_idx=model.index(row, 0, parent)
            match=self.find(idx, model, title_idx)
            if match and match.isValid():
                return match

    def updateHeaderRatio(self):
        header=self.m_view.header()
        width=self.m_view.size().width()
        for col, weight in self.section_ratios.items():
            header.resizeSection(
                    col, int(width*weight))

    def setupView(self):
        self.m_view=self.app.buffman.createView(
                OutlineView, None)
        self.app.stateman.viewChanged.connect(
                self.updateOutline)
        self.m_view.resized.connect(
                self.updateHeaderRatio)

    @tag('<c-O>(normal/outline)')
    def toggleOutline(self):
        self.m_view.toggle()

    @tag('o(normal)[OutlineView]')
    def open(self, view=None, focus=False):
        if not view:
            view=self.app.stateman.subview()
        item=self.m_view.currentItem()
        if item and view:
            data=item.data()
            self.app.delegman.delegate(
                    'normal', None, view, 'goTo', **data)
            if focus:
                view.activate()

    @tag('O(normal)[OutlineView]')
    def openAndFocus(self, *args, **kwargs):
        kwargs['focus']=True
        self.open(*args, **kwargs)
