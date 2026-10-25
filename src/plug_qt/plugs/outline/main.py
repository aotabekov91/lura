from PyQt6 import QtCore

from plug import Plug, tag

from .view import OutlineView

class Outline(Plug):

    column_ratios={0: .75, 1: .25}

    def setup(self):
        super().setup()
        self.m_subview=None
        self.setupView()

    def setupView(self):
        self.m_view=self.app.buffman.createView(
                OutlineView, None)
        self.app.stateman.viewChanged.connect(
                self.updateOutline)
        self.m_view.resized.connect(
                self.updateHeaderRatio)

    def updateOutline(self, view):
        if view:
            model=view.model()
            outline=self.app.delegman.delegate(
                    mode='normal', 
                    action='getOutline', 
                    model=model,
                    data={'model': model})
            if outline:
                self.m_view.setModel(outline)
                self.connectView(view)
                self.updateHeaderRatio()

            else:
                self.m_view.setModel(None)

    def connectView(self, view=None):
        if self.m_subview:
            self.m_subview.indexChanged.disconnect(
                    self.updateOutlineIndex)
        self.m_subview=view
        if self.m_subview:
            self.m_subview.indexChanged.connect(
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
        for col, weight in self.column_ratios.items():
            header.resizeSection(
                    col, int(width*weight))

    @tag('<c-O>(normal/outline)')
    def toggleOutline(self):
        self.m_view.toggle()

    @tag('o(normal)[OutlineView]')
    def open(self, view=None, focus=False):
        view = view or self.app.stateman.subview()
        if view:
            item=self.m_view.currentItem()
            if item:
                data=item.data()
                self.app.delegman.delegate(
                        mode='normal', 
                        view=view, 
                        action='goTo', 
                        data=data)
                if focus:
                    view.activate()

    @tag('O(normal)[OutlineView]')
    def openAndFocus(self, *args, **kwargs):
        kwargs['focus']=True
        self.open(*args, **kwargs)
