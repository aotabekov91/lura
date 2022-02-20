from .config import getConfiguration

from lura.core.widgets import Menu

class ToggleMenu(Menu):

    def __init__(self, parent):
        super().__init__(parent, commando=getConfiguration('ToggleMenu'))
        self.m_tree=parent.m_view
        self.setHeight(200)

    def toggleQuote(self):
        self.hide()
        self.m_tree.setFocus()
        self.m_tree.currentItem().proxy().toggle('quote')

    def toggleAuthor(self):
        self.hide()
        self.m_tree.setFocus()
        self.m_tree.currentItem().proxy().toggle('author')

    def toggleColor(self):
        self.hide()
        self.m_tree.setFocus()
        self.m_tree.currentItem().proxy().toggle('color')

    def toggleMeta(self):
        self.hide()
        self.m_tree.setFocus()
        self.m_tree.currentItem().proxy().toggle('meta')

    def toggleTag(self):
        self.hide()
        self.m_tree.setFocus()
        self.m_tree.currentItem().proxy().toggle('tag')

    def toggleId(self):
        self.hide()
        self.m_tree.setFocus()
        self.m_tree.currentItem().proxy().toggle('id')

    def toggleContent(self):
        self.hide()
        self.m_tree.setFocus()
        self.m_tree.currentItem().proxy().toggle('content')
