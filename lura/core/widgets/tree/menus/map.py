from .config import getConfiguration

from lura.core.widgets import Menu
from lura.core.widgets.tree import Item

class MapMenu(Menu):

    def __init__(self, parent):
        super().__init__(parent, commando=getConfiguration('MapMenu'))
        self.m_tree=parent.m_view
        self.setHeight(200)

    def addContainer(self):
        self.hide()
        item=self.m_tree.currentItem()
        if item is None: item=self.m_tree.model().invisibleRootItem()
        self.m_tree.model().addContainer(item)
        self.m_tree.setFocus()

    def addNote(self):
        self.hide()
        sItem=self.m_tree.currentItem()
        note=self.m_parent.window.plugin.notes.new()
        if self.m_parent.window.view() is not None:
            did=self.m_parent.window.document().id()
            page=self.m_parent.window.view().currentPage()
            left, top=self.m_parent.window.view().saveLeftAndTop()
            tags=f'did:{did}; did:{did}:{page}:{left}:{top}'
            note.setTags(tags)
        self.m_tree.model().itemParent(sItem).insertRow(sItem.row()+1, Item(note))
        self.m_tree.setFocus()
