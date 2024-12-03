from plug import Plug, tag

from .view import OutlineView

class Outline(Plug):

    section_ratios={0: .75, 1: .25}

    def setup(self):
        super().setup()
        self.m_outliners={}
        self.m_current_view=None
        self.setupView()

    # def updateOutlineIndex(self, view):
    #     # view_model=view.model()
    #     idx=view.currentIndex()
    #     tree_model=self.view.model()
    #     # self.findOutlineIndex(tree_model, QModelIndex(), idx)
    #     found=self.find(idx, tree_model)
    #     print(found)
    #     self.view.setCurrentIndex(found)

    # def findOutlineIndex(self, model, parent_idx, idx):
    #     for i in range(model.rowCount(parent_idx)):
    #         child_idx=model.index(i, 0, parent_idx)
    #         page_idx=model.index(i, 1, parent_idx)
    #         data=model.data(page_idx)
    #         if idx and data: 
    #             data=int(data)
    #             if data<=idx:
    #                 print(data, idx)
    #         if model.hasChildren(child_idx):
    #             self.findOutlineIndex(model, child_idx, idx)

    # def find(self, item, model, parent=None):
    #     root=model.invisibleRootItem()
    #     print(root.rowCount())
    #     if root.rowCount()>0: 
    #         if not parent: 
    #             parent=model.indexFromItem(root.child(0,0))
    #         for row in range(model.rowCount(parent)):
    #             index=model.index(row, 0, parent)
    #             if index==model.indexFromItem(item): 
    #                 return index
    #         print(model.rowCount(parent))
    #         for row in range(model.rowCount(parent)):
    #             index=model.index(row, 0, parent)
    #             match=self.sync(item, model, index)
    #             if match.isValid():
    #                 return match
    #         return model.indexFromItem(root.child(0,0))

    # def sync(self, page, model, parent):
    #     raise
    #     for row in range(model.rowCount(parent)):
    #         index=model.index(row, 0, parent)
    #         data=model.index(row, 1, parent)
    #         print(data, page)
    #         if page==data: 
    #             return index
    #     for row in range(model.rowCount(parent)):
    #         index=model.index(row, 0, parent)
    #         match=self.sync(page, model, index)
    #         if match.isValid():
    #             return match
    #     return QModelIndex()

    def updateOutline(self, view):
        model=view.model()
        name=model.__class__.__name__
        outliner=self.outliner(name)
        if outliner:
            outline=outliner.getOutline(model)
            if outline:
                self.view.setModel(outline)
                # self.updateOutlineIndex(view)

    def updateHeaderRatio(self):
        header=self.view.header()
        width=self.view.size().width()
        for col, weight in self.section_ratios.items():
            header.resizeSection(
                    col, int(width*weight))

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

    @tag('<c-o>(normal/outline)')
    def toggleOutline(self):
        self.view.toggle()

    @tag('o(normal)[OutlineView]')
    def open(self, view=None, focus=False):
        item=self.view.currentItem()
        normal=self.app.plugman.getPlug('Normal')
        if not view:
            view=self.app.stateman.subview()
        if item and normal:
            data=item.data()
            normal.activate(action='goTo', view=view, **data)
            if focus:
                view.activate()

    @tag('O(normal)[OutlineView]')
    def openAndFocus(self, *args, **kwargs):
        kwargs['focus']=True
        self.open(*args, **kwargs)
