import os
from collections import Counter

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.core import Item
from lura.core import MapTree

class MapView(QWidget):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent
        self.setup()

    def setup(self):

        self.chosenFor=None

        self.m_layout = QVBoxLayout(self)
        self.m_layout.setSpacing(0)
        self.m_layout.setContentsMargins(0,0,0,0)
        self.m_title = MQLineEdit()

        self.m_view = MapTree(self, self.window)
        self.m_view.open = self.openNode
        self.m_view.currentItemChanged.connect(
                self.window.mapItemChanged)
        # self.m_view.currentItemChanged.connect(
                # self.on_currentItemChanged)

        self.m_tagView=MapTree(self, self.window)
        self.m_tagView.open = self.openNode
        self.m_tagView.currentItemChanged.connect(
                self.window.mapItemChanged)

        self.m_tagView.hide()

        commandList=[
                ('maf', 'addFolder'),
                ('mad', 'addDocument'),
                ('mdd', 'deleteDocument'),
                ('maw', 'addWatchFolder'),
                ('muw', 'updateWatchFolder'),
                ('msa', 'activateSorting'),
                ('msd', 'deactivateSorting'),
                ('mfa', 'activateFiltering'),
                ('mfd', 'deactivateFiltering'),
                ('mtt', 'showTagTree'),
                ('mmd', 'moveDocumentTo'),
                ]
        self.window.plugin.command.addCommands(commandList, self)

        self.m_layout.addWidget(self.m_title)
        self.m_layout.addWidget(self.m_view)
        self.m_layout.addWidget(self.m_tagView)

        self.fuzzy = self.window.plugin.fuzzy
        self.fuzzy.fuzzySelected.connect(self.addDocument)

        self.window.titleChanged.connect(self.updateTitles)
        self.window.plugin.fileBrowser.pathChosen.connect(self.actOnChoosen)


    def tree(self):
        return self.m_view

    def activateSorting(self):
        if self.m_view.model() is None: return
        self.m_view.setProxyModel(self.m_proxyModel)
        self.m_view.sortByColumn(0, Qt.AscendingOrder)
        self.m_view.setFocus()

    def deactivateSorting(self):
        if self.m_view.model() is None: return
        self.m_view.setModel(self.m_document.m_model)
        self.m_view.setFocus()

    def activateFiltering(self):
        if self.m_view.model() is None: return
        self.m_view.setProxyModel(self.m_proxyModel)
        self.window.plugin.command.activateCustom(
                self._activateFiltering, 'Filter: ', self._activateFiltering)

    def _activateFiltering(self, text):
        if self.m_view.model() is None: return
        self.m_proxyModel.setFilterFixedString(text)
        self.m_view.setFocus()

    def deactivateFiltering(self):
        if self.m_view.model() is None: return
        self.m_view.setModel(self.m_document.m_model)
        self.m_view.setFocus()

    def addAnnotations(self, item):
        annotations = self.window.plugin.tables.get(
                'annotations', {'did': item.id()}, unique=False)
        if annotations is None: return
        for a in annotations:
            aItem = Item('annotation', a['id'], self.window)
            if not self.isChild(aItem, item): 
                item.appendRow(aItem)

    def isChild(self, child, possibleParent, recursively=False):
        for index in range(possibleParent.rowCount()):
            p=possibleParent.child(index)
            if child == p: return p
            if recursively: 
                r=self.isChild(child, p, recursively)
                if r: return r
        return None

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

        self.m_proxyModel=QSortFilterProxyModel(self.m_view)
        self.m_proxyModel.setSourceModel(self.m_document.m_model)
        self.m_proxyModel.setDynamicSortFilter(True)

        self.show()
        self.m_view.show()
        self.m_view.setFocus()

        self.updateWatchFolder()
        self.m_title.setMap(document.id(), self.window)

    def actOnChoosen(self, chosen):
        if self.chosenFor=='addWatchFolder':
            self.addWatchFolder(chosen)
        elif self.chosenFor=='addFolder':
            self.addFolder(chosen)

    def updateWatchFolder(self):

        root=self.m_document.m_model.invisibleRootItem()

        wCon=None
        for i in range(root.rowCount()):
            child=root.child(i)
            if child.kind()=='container' and child.get('title')=='Documents':
                wCon=child
                break

        if wCon is None: return

        for path in wCon.watchFolder():
            qIterator = QDirIterator(
                path, ["*.pdf", "*PDF"], QDir.Files, QDirIterator.Subdirectories)

            while qIterator.hasNext():
                loc=qIterator.next()
                self.addDocument(loc, client=self, item=wCon, recursively=True)

        toRemove=[]
        for i in range(wCon.rowCount()):
            item=wCon.child(i)
            if not item.kind()=='document': continue
            loc=self.window.plugin.tables.get('documents',
                    {'id':item.id()}, 'loc')
            if loc is None: continue
            if os.path.exists(loc): continue
            toRemove+=[item]

        for item in toRemove:
            self.m_view.delete(item)

    def addWatchFolder(self, path=False):
        if not self.isVisible(): return

        if not path:

            self.chosenFor='addWatchFolder'
            self.window.plugin.fileBrowser.toggle()

        else:

            self.chosenFor=None
            self.window.plugin.fileBrowser.toggle()

            wCon=None
            root=self.m_document.m_model.invisibleRootItem()
            for i in range(root.rowCount()):
                child=root.child(i)
                if child.kind()=='container' and child.get('title')=='Documents':
                    wCon=child
                    break
            if not wCon:
                wCon=Item('container', None, self.window, 'Documents')
                root.insertRow(0, wCon)

            if os.path.isdir(path):
                wCon.addWatchFolder(path)
                qIterator = QDirIterator(
                    path, ["*.pdf", "*PDF"], QDir.Files, QDirIterator.Subdirectories)
                while qIterator.hasNext():
                    self.addDocument(qIterator.next(), client=self, item=wCon)

            self.m_view.setFocus()

    def deleteDocument(self):
        item=self.m_view.currentItem()
        if item is None: return
        if item.kind()!='document': return

        
        self.window.plugin.command.activateCustom(
                self._deleteDocument, 
                'Do you want to delete the document [yes/no]: ')

    def _deleteDocument(self, text):
        if text!='yes': return
        item=self.m_view.currentItem()
        if item is None: return
        if item.kind()!='document': return

        loc=self.window.plugin.tables.get('documents', {'id':item.id()}, 'loc')

        # from map
        self.m_view.delete(item)
        # from annotations
        self.window.plugin.tables.remove('annotations', {'did':item.id()})
        # from metadata
        self.window.plugin.tables.remove('metadata', {'did':item.id()})
        # from documents
        self.window.plugin.tables.remove('documents', {'id':item.id()})
        # from the system
        self.window.closeView(loc)
        os.remove(loc)

        self.setFocus()

    def moveDocumentTo(self):
        item=self.m_view.currentItem()
        if item is None or item.kind()!='document': return

        filePath=self.window.plugin.tables.get(
                'documents', {'id':item.id()}, 'loc')
        dirLoc=filePath.rsplit('/', 1)[0]

        self.window.plugin.command.activateCustom(
                self._moveDocumentTo, 'Move to: ', text=dirLoc)

    def _moveDocumentTo(self, text):
        item=self.m_view.currentItem()
        if item is None or item.kind()!='document': return

        oldFilePath=self.window.plugin.tables.get(
                'documents', {'id':item.id()}, 'loc')
        fileName=oldFilePath.rsplit('/', 1)[-1]

        if not text.endswith('/'): text+='/'

        if not os.path.exists(text): return
        newFilePath=text+fileName

        os.rename(oldFilePath, newFilePath)
        self.window.plugin.tables.update(
                'documents', {'id':item.id()}, {'loc':newFilePath})

        parent=item.parent()
        if parent is None: parent=self.m_view.model().invisibleRootItem()
        parent.takeRow(item.row())

        self.setFocus()


    def addFolder(self, path=False):

        if not self.isVisible(): return

        if not path:

            self.chosenFor='addFolder'
            self.window.plugin.fileBrowser.toggle()

        else:

            self.chosenFor=None
            self.window.plugin.fileBrowser.toggle()
            if os.path.isdir(path):
                qIterator = QDirIterator(
                    path, ["*.pdf", "*PDF"], QDir.Files, QDirIterator.Subdirectories)
                while qIterator.hasNext():
                    self.addDocument(qIterator.next(), client=self)
            else:
                self.addDocument(path, client=self)

            self.m_view.setFocus()

    def addDocument(self, selected=False, client=False, item=None,
            recursively=False):

        if not self.isVisible(): return

        if not selected:

            self.window.plugin.documents.getFuzzy(self)

        else:

            if client != self: return
            self.fuzzy.deactivate(self)

            document = self.window.buffer.loadDocument(selected)
            if document is None: return
            did = document.id()

            if item is None:
                item = self.m_view.currentItem()
                if item is None:
                    item = self.m_document.m_model.invisibleRootItem()
            dItem = Item('document', did, self.window)

            myDItem=self.isChild(dItem, item, recursively)
            if myDItem is None: 
                item.appendRow(dItem)
                myDItem=dItem
            self.addAnnotations(myDItem)

    def save(self):
        pass

    def openNode(self, item=None):

        if item is None: item = self.m_view.currentItem()

        if item is None: return

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
            item=self.m_document.m_model.invisibleRootItem()
        for index in range(item.rowCount()):
            self.updateMap(item.child(index))
        if item!=self.m_document.m_view.invisibleRootItem():
            if item.kind()!='container':
                r=self.window.plugin.tables.get(
                        item.kind(), {'id':item.id()}, 'id')
                if r is None:
                    parent=item.parent()
                    if parent is None: parent=self.m_document.m_model.invisibleRootItem()
                    parent.takeRow(item.row())
            if item.kind()=='document':
                self.addAnnotations(item)

    def updateTitles(self, sender):
        if sender==self: return
        self._updateTitles(sender=sender)

    def showTagTree(self):
        if self.m_view.model() is None: return
        self.window.plugin.tags.showTagsFromModel(self.m_document.m_model)

    def _updateTitles(self, item=None, sender=None):
        if not self.m_view.isVisible(): return
        if item is None:
            item=self.m_document.m_model.invisibleRootItem()
        for index in range(item.rowCount()):
            self._updateTitles(item.child(index), sender)
        if item!=self.m_document.m_model.invisibleRootItem():
            item.setTitle()

    # open node on item change in docviewer
    # if set so in the settings
    def on_currentItemChanged(self, item):
        if not self.window.isDocumentViewVisible(): return
        if True: return
        self.openNode(item)
        self.setFocus()

    def on_itemChanged(self, item):
        item.update()
        if item.kind() == 'container':
            self.m_document.update()
        if item.m_changedFromOutside:
            item.m_changedFromOutside=False
            return
        self.window.titleChanged.emit(self)

    def event(self, event):
        if event.type()==QEvent.Enter: self.window.setView(self)
        return super().event(event)

class MQLineEdit(QLineEdit):

    def __init__(self):
        super().__init__()
        self.textChanged.connect(self.on_textChanged)

    def setMap(self, m_id, window):
        self.window=window
        self.m_id=m_id
        self.setText(self.window.plugin.tables.get(
            'maps', {'id':self.m_id}, 'title'))

    def on_textChanged(self, text):
        self.window.plugin.tables.update(
                'maps', {'id':self.m_id}, {'title':text})
