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
        self.window=parent
        self.s_settings=settings['MindMapView']

        self.setup()

    def setup(self):

        self.m_layout=QVBoxLayout(self)
        self.m_view=CustomTreeMap(self)

        self.m_mapMenu=MapMenu(self)
        self.m_itemMenu=ItemMenu(self)
        self.m_changeMenu=ChangeMenu(self)
        self.m_toggleMenu=ToggleMenu(self)
        self.m_sortMenu=SortMenu(self)
        self.m_quickmark=Quickmark(self)
        self.m_filter=Filter(self)

        # self.m_view.buttonClicked.connect(self.m_itemMenu.open)

        self.m_layout.addWidget(self.m_view)
        self.m_layout.addWidget(self.m_mapMenu)
        self.m_layout.addWidget(self.m_itemMenu)
        self.m_layout.addWidget(self.m_changeMenu)
        self.m_layout.addWidget(self.m_toggleMenu)
        self.m_layout.addWidget(self.m_sortMenu)
        self.m_layout.addWidget(self.m_quickmark)
        self.m_layout.addWidget(self.m_filter)

        self.hideMenus()

        self.fuzzy = self.window.plugin.fuzzy
        self.fuzzy.fuzzySelected.connect(self.addDocument)

        self.setActions()
        self.adjustMapMenu()
        self.setRenameEdit()

    def adjustMapMenu(self):
        mapMapping={getattr(self, f):v for f,v in self.s_settings['MapMenu'].items()}
        self.m_mapMenu.addActions(mapMapping)

    def hideMenus(self):
        self.m_mapMenu.hide()
        self.m_itemMenu.hide()
        self.m_changeMenu.hide()
        self.m_toggleMenu.hide()
        self.m_sortMenu.hide()

    def mark(self):
        self.m_quickmark.get()

    def go(self):
        self.m_quickmark.set()

    def filter(self):
        self.m_filter.toggle()

    def unfilter(self):
        self.m_view.unfilter()

    def setRenameEdit(self):
        self.renameWidget=QWidget()
        label=QLabel('Rename map')
        self.renameEdit=QLineEdit()
        self.renameEdit.returnPressed.connect(lambda: self.renameMap(act=True))
        layout=QHBoxLayout(self.renameWidget)
        layout.addWidget(label)
        layout.addWidget(self.renameEdit)

    def renameMap(self, act=False):
        if not act:
            self.hideMenus()
            self.renameEdit.setText(self.m_document.title())
            self.window.activateStatusBar(self.renameWidget)
            self.renameWidget.show()
            self.renameEdit.setFocus()
        else:
            self.window.deactivateStatusBar(self.renameWidget)
            self.m_document.setTitle(self.renameEdit.text())
            self.setFocus()

    def setActions(self):
        self.actions=[]
        for func, key in self.s_settings['shortcuts'].items():

            m_action=QAction(f'({key}) {func}')
            m_action.setShortcut(QKeySequence(key))
            m_action.setShortcutContext(Qt.WidgetWithChildrenShortcut)
            self.actions+=[m_action]
            m_action.triggered.connect(getattr(self, func))
            self.m_view.addAction(m_action)

    def updateMap(self):
        self.hideMenus()
        dItems=self.m_document.findItemByKind('document')
        for dItem in dItems:
            self.addAnnotations(dItem)
            self.addNotes(dItem)

    def addNotes(self, item):
        nContainer=self.m_document.findOrCreateContainer('Notes', item)
        for note in self.window.plugin.notes.getByDid(item.itemData().id()):
            nItem=Item(note)
            if self.m_document.isChild(nItem, nContainer): continue
            nContainer.appendRow(nItem)

    def addAnnotations(self, item):
        aContainer=self.m_document.findOrCreateContainer('Annotations', item)
        # for annotation in item.itemData().annotations():
        condition={'field':'did', 'value': item.itemData().id()}
        annotations=self.window.plugin.annotation.getBy(condition)
        for annotation in annotations:
            aItem=Item(annotation)
            if self.m_document.isChild(aItem, aContainer): continue
            aContainer.appendRow(aItem)

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
        self.m_document=document
        self.m_document.annotationAdded.connect(self.addAnnotations)

        self.hide()
        self.m_view.hide()
        self.m_view.setModel(self.m_document.m_model)

        self.show()
        self.m_view.show()
        self.m_view.setFocus()

    def addFolder(self, path=False):

        self.hideMenus()

        if not path:
            self.window.plugin.fileBrowser.pathChosen.connect(self.addFolder)
            self.window.plugin.fileBrowser.toggle()

        else:
            self.window.plugin.fileBrowser.toggle()
            if not os.path.isdir(path): return
            qIterator= QDirIterator(path, ["*.pdf", "*PDF"], QDir.Files, QDirIterator.Subdirectories)
            while qIterator.hasNext():
                self.addDocument(qIterator.next(), client=self)
            
    def addLiterature(self):

        self.hideMenus()

        allAnnotations=self.m_document.findItemByKind('annotation')
        lContainer=self.m_document.findOrCreateContainer('Literature')
        colorSystem=self.window.plugin.annotation.colorSystem()
        lColor=colorSystem['Literature'].lower()

        for aItem in allAnnotations:
            if aItem.itemData().color().name()!=lColor: continue
            if self.m_document.isChild(aItem, lContainer): continue

            content=aItem.itemData().content()
            if content is None: content=''
            aItem.itemData().setTitle(content)

            lContainer.appendRow(aItem.copy())

    def addDocument(self, selected=False, client=False):
        if not selected:

            self.hideMenus()
            self.kind='documents'
            self.window.plugin.documents.getFuzzy(self)

        else:

            if client!=self: return
            self.fuzzy.deactivate(self)
            document=self.window.buffer.loadDocument(selected)
            if document is None: return

            dItem=Item(document)
            dContainer=self.m_document.findOrCreateContainer('Documents')
            if self.m_document.isChild(dItem, dContainer): return
            dContainer.appendRow(dItem)

            self.addAnnotations(dItem)
            self.addNotes(dItem)

    def toggleMapMenu(self):
        self.hideMenus()
        self.m_mapMenu.toggle()

    def toggleItemMenu(self):
        if self.m_view.currentItem() is None: return
        self.hideMenus()
        self.m_itemMenu.toggle()

    def toggleChangeMenu(self):
        if self.m_view.currentItem() is None: return
        self.hideMenus()
        self.m_changeMenu.toggle()

    def toggleMetaMenu(self):
        if self.m_view.currentItem() is None: return
        self.hideMenus()
        self.m_toggleMenu.toggle()

    def toggleSortMenu(self):
        if self.m_view.currentItem() is None: return
        self.hideMenus()
        self.m_sortMenu.toggle()

    def save(self):
        pass

    def keyPressEvent(self, event):
        print(self.__class__.__name__)
        if event.key()==Qt.Key_Q:
            self.window.close()
