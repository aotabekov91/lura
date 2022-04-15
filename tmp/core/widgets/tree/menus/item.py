from .config import getConfiguration

from lura.core.widgets import Menu

class ItemMenu(Menu):

    def __init__(self, parent):
        super().__init__(parent, commando=getConfiguration('ItemMenu'))
        self.m_parent=parent
        self.m_tree=parent.m_view
        self.setHeight(200)

    def delete(self):
        self.hide()
        self.m_parent.deleteNode()

    def open(self):
        self.hide()
        self.m_parent.openNode()

    def yank(self):
        self.hide()
        self.m_parent.yankNode()

    def copy(self):
        self.hide()
        self.m_parent.copyNode()

    def pasteInside(self):
        self.hide()
        self.m_parent.pasteNodeInside()
