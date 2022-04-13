from .config import getConfiguration

from lura.core.widgets import Menu

class ItemMenu(Menu):

    def __init__(self, parent):
        super().__init__(parent, commando=getConfiguration('ItemMenu'))
        self.m_tree=parent.m_view
        self.setHeight(200)

    def delete(self):
        self.hide()
        self.m_tree.delete()

    def open(self):
        self.openWithFocus()
        self.m_tree.setFocus()

    def openWithFocus(self):
        self.hide()
        item=self.m_tree.currentItem()

        if item.itemData().getField('kind')=='annotation':

            document=item.itemData().page().document()
            pageNumber=item.itemData().page().pageNumber()

            self.m_parent.window.open(document.filePath())
            left, top=item.itemData().leftTop()
            self.m_parent.window.view().jumpToPage(pageNumber, left, top)

        elif item.itemData().getField('kind')=='document':
            filePath=self.m_parent.window.plugin.tables.get(
                    'documents', {'id':item.itemData().id()}, 'loc')
            if filePath is None: return
            self.m_parent.window.open(filePath)

    def openInWeb(self):
        self.hide()
        item=self.m_tree.currentItem()
        self.m_tree.window.search(item.itemData().title())
        self.m_tree.setFocus()
