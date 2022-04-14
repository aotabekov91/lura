import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.core.widgets import Menu
from lura.core.widgets.tree import Item
from lura.core.widgets.tree import Container

from lura.core.widgets.tree.menus import MapMenu
from lura.core.widgets.tree.menus import ItemMenu
from lura.core.widgets.tree.menus import SortMenu
from lura.core.widgets.tree.menus import ChangeMenu
from lura.core.widgets.tree.menus import ToggleMenu

# from lura.core.widgets.tree import TreeView
from lura.core.widgets.custom import CustomTreeMap

from lura.core.widgets import Filter
from lura.core.widgets import Quickmark


class MapView(QWidget):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent
        self.s_settings = settings['MindMapView']

        self.setup()

    def setup(self):

        self.m_layout = QVBoxLayout(self)
        self.m_layout.setSpacing(0)
        self.m_title = QLineEdit('Mindmap')
        self.m_view = CustomTreeMap(self)

        self.m_view.open = self.openNode
        self.m_view.update = self.updateMap

        self.m_layout.addWidget(self.m_title)
        self.m_layout.addWidget(self.m_view)

        self.fuzzy = self.window.plugin.fuzzy
        self.fuzzy.fuzzySelected.connect(self.addDocument)

        self.setActions()

    def setActions(self):
        self.actions = []
        for func, key in self.s_settings['shortcuts'].items():

            m_action = QAction(f'({key}) {func}')
            m_action.setShortcut(QKeySequence(key))
            m_action.setShortcutContext(Qt.WidgetWithChildrenShortcut)
            self.actions += [m_action]
            m_action.triggered.connect(getattr(self, func))
            self.m_view.addAction(m_action)


    def addAnnotations(self, item):
        annotations = self.window.plugin.tables.get(
            'annotations', {'did': item.id()}, unique=False)
        if annotations is None:
            return
        for a in annotations:
            aItem = Item('annotation', a['id'], self.window)
            if self.isChild(aItem, item): continue
            item.appendRow(aItem)

    def isChild(self, child, possibleParent):
        for index in range(possibleParent.rowCount()):
            p=possibleParent.child(index)
            if child == p: return True
        return False

    def readjust(self):
        pass

    def fitToPageWidth(self):
        pass

    def setFocus(self):
        self.m_view.setFocus()

    def document(self):
        return self.m_document

    def open(self, document):

        self.setFocus()
        self.m_document = document

        self.hide()
        self.m_view.hide()
        self.m_view.setModel(self.m_document.m_model)
        self.m_view.model().itemChanged.connect(self.on_itemChanged)

        self.show()
        self.m_view.show()
        self.m_view.setFocus()

    def addFolder(self, path=False):

        if not path:

            self.window.plugin.fileBrowser.pathChosen.connect(self.addFolder)
            self.window.plugin.fileBrowser.toggle()

        else:

            self.window.plugin.fileBrowser.toggle()
            self.setFocus()
            if os.path.isdir(path):
                qIterator = QDirIterator(
                    path, ["*.pdf", "*PDF"], QDir.Files, QDirIterator.Subdirectories)
                while qIterator.hasNext():
                    self.addDocument(qIterator.next(), client=self)
            else:
                self.addDocument(path, client=self)


    def addDocument(self, selected=False, client=False):
        if not selected:

            self.window.plugin.documents.getFuzzy(self)

        else:

            if client != self: return
            self.fuzzy.deactivate(self)

            did = self.window.plugin.tables.get(
                'documents', {'loc': selected}, 'id')
            if did is None:
                document = self.window.buffer.loadDocument(selected)
                did = document.id()
            dItem = Item('document', did, self.window)
            item = self.m_view.currentItem()
            if item is None:
                item = self.m_view.model().invisibleRootItem()
            if self.isChild(dItem, item): return

            item.appendRow(dItem)
            self.addAnnotations(dItem)

    def save(self):
        pass

    def openNode(self):
        item = self.m_view.currentItem()

        if item.kind() == 'annotation':

            b = item.get('position').split(':')
            topLeft = QPointF(float(b[0]), float(b[1]))
            did = item.get('did')
            pageNumber = item.get('page')
            filePath = self.window.plugin.tables.get(
                'documents', {'id': did}, 'loc')

            self.window.open(filePath)
            self.window.view().jumpToPage(
                pageNumber, topLeft.x(), 0.95*topLeft.y())

        elif item.kind() == 'document':

            filePath = self.window.plugin.tables.get(
                'documents', {'id': item.id()}, 'loc')
            self.window.open(filePath)

    def updateMap(self, item=None):
        if item is None:
            item=self.m_view.model().invisibleRootItem()
        for index in range(item.rowCount()):
            self.updateMap(item.child(index))
        if item!=self.m_view.model().invisibleRootItem():
            if item.kind()=='document':
                self.addAnnotations(item)

    def on_itemChanged(self, item):
        item.update()
        if item.kind() == 'container':
            self.m_document.update()
