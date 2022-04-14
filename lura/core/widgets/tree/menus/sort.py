from .config import getConfiguration

from lura.core.widgets import Menu
from lura.core.widgets.tree import Item

class SortMenu(Menu):

    def __init__(self, parent):
        super().__init__(parent, commando=getConfiguration('SortMenu'))
        self.m_tree=parent.m_view
        self.setHeight(200)

    def sortByTitle(self):
        self.hide()
        item=self.m_tree.currentItem()

        parent=item.parent()
        if parent is None: parent=self.m_tree.model().invisibleRootItem()

        children=[]
        titles=[]

        for index in range(item.rowCount()):
            children+=[item.child(index)]
            titles+=[item.child(index).itemData().title()]

        sortedChildren=[x for _, x in sorted(zip(titles, children), key=lambda pair: pair[0])]

        copy=item.copy(shallow=True)
        for child in sortedChildren:
            copy.appendRow(child.copy())

        parent.insertRow(item.row(), copy)
        parent.takeRow(item.row())

        self.m_tree.setFocus()

    def sortByContent(self):
        self.hide()
        item=self.m_tree.currentItem()

        parent=item.parent()
        if parent is None: parent=self.m_tree.model().invisibleRootItem()

        children=[]
        contents=[]

        for index in range(item.rowCount()):
            children+=[item.child(index)]
            if not hasattr(item.child(index).itemData, 'content'): return
            contents+=[item.child(index).itemData().contents()]

        sortedChildren=[x for _, x in sorted(zip(contents, children), key=lambda pair: pair[0])]

        copy=item.copy(shallow=True)
        for child in sortedChildren:
            copy.appendRow(child.copy())

        parent.insertRow(item.row(), copy)
        parent.takeRow(item.row())

        self.m_tree.setFocus()

    def sortByPageNumber(self):
        self.hide()
        item=self.m_tree.currentItem()

        parent=item.parent()
        if parent is None: parent=self.m_tree.model().invisibleRootItem()

        children=[]
        pageNumbers=[]

        for index in range(item.rowCount()):
            children+=[item.child(index)]
            if not hasattr(item.child(index).itemData, 'page'): return
            pageNumbers+=[item.child(index).itemData().page().pageNumber()]

        sortedChildren=[x for _, x in sorted(zip(pageNumbers, children), key=lambda pair: pair[0])]

        copy=item.copy(shallow=True)
        for child in sortedChildren:
            copy.appendRow(child.copy())

        parent.insertRow(item.row(), copy)
        parent.takeRow(item.row())

        self.m_tree.setFocus()

    def sortByCreateDate(self):
        pass
