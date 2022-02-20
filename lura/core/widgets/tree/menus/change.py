from .config import getConfiguration

from lura.core.widgets import Menu

class ChangeMenu(Menu):

    def __init__(self, parent):
        super().__init__(parent, commando=getConfiguration('ChangeMenu'))
        self.m_tree=parent.m_view
        self.setHeight(200)

    def changeTag(self):
        self.hide()
        self.m_tree.setFocus()
        self.m_tree.currentItem().proxy().change('tag')

    def changeTitle(self):
        self.hide()
        self.m_tree.setFocus()
        self.m_tree.currentItem().proxy().change('title')

    def changeContent(self):
        self.hide()
        self.m_tree.setFocus()
        self.m_tree.currentItem().proxy().change('content')

    def changeAuthor(self):
        self.hide()
        self.m_tree.setFocus()
        self.m_tree.currentItem().proxy().change('author')

