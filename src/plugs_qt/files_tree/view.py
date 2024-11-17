from plug_qt.vimo import mixin
from plug_qt.vimo.gizmo.view.tree import TreeView

class FilesView(
        mixin.view.TreeGo,
        TreeView
        ):

    position = {"FilesView": "D|L"}


    #     self.app.main.display.viewChanged.connect(self.on_viewChanged)
    #     self.app.main.display.itemChanged.connect(self.on_viewItemChanged)


    # def __init__(self, app): 
    #     super().__init__(app, position='left', mode_keys={'command':'o'})

    # def setUI(self):

    #     super().setUI()

    #     self.ui.main.tree.m_expansionRole=Qt.UserRole+4
    #     self.ui.main.tree.m_expansionIDRole=Qt.UserRole+5

    #     self.ui.main.tree.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #     self.ui.main.tree.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
    #     self.ui.main.tree.header().setSectionResizeMode(QHeaderView.Interactive)

    # def on_outlineClicked(self, index=None):

    #     if index is None: index=self.ui.main.tree.currentIndex()
    #     if index:
    #         page=index.data(Qt.UserRole+1)
    #         left=index.data(Qt.UserRole+2)
    #         top=index.data(Qt.UserRole+3)

    #         self.app.main.display.itemChanged.disconnect(self.on_viewItemChanged)
    #         self.app.main.display.currentView().goto(page, left, top)
    #         self.app.main.display.itemChanged.connect(self.on_viewItemChanged)

    # def on_viewItemChanged(self, model, pageItem):

    #     if self.outline:
    #         page=pageItem.page().pageNumber()
    #         found=self.find(page, self.outline)
    #         if found: self.ui.main.tree.setCurrentIndex(found)

    # def setData(self):

    #     self.outline=None
    #     view=self.app.main.display.view
    #     if view:
    #         document=view.model()
    #         self.outline=document.loadOutline()
    #         self.ui.main.tree.setModel(self.outline)
    #         print(self.outline.invisibleRootItem().rowCount())

    # def activate(self):

    #     self.setData()

    #     self.app.main.display.viewChanged.connect(self.on_viewChanged)
    #     self.app.main.display.itemChanged.connect(self.on_viewItemChanged)

    #     super().activate()

    # def deactivate(self):

    #     self.app.main.display.viewChanged.disconnect(self.on_viewChanged)
    #     self.app.main.display.itemChanged.disconnect(self.on_viewItemChanged)

    #     super().deactivate()
