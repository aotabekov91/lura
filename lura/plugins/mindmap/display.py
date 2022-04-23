import os
from collections import Counter

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.core import Item
from lura.core import MapTree

class MapView(MapTree):

    def __init__(self, parent, window):
        super().__init__(window, window)
        self.m_parent=parent
        self.window = window
        self.location='left'
        self.name='mapview'
        self.setup()

    def setup(self):

        self.chosenFor=None

        commandList=[
                ('maf', 'addFolder'),
                ('mad', 'addDocument'),
                ('mdd', 'deleteDocument'),
                ('mmd', 'moveDocumentTo'),
                ('maw', 'addWatchFolder'),
                ('mtv', 'showTagView'),
                ]

        self.window.plugin.command.addCommands(commandList, self)

        self.window.titleChanged.connect(self.updateTitles)
        self.window.plugin.fileBrowser.returnPressed.connect(self.actOnChoosen)

        self.currentItemChanged.connect(self.window.mapItemChanged)
        self.window.setTabLocation(self, self.location, self.name)

    def showTagView(self):
        if self.model() is None: return
        self.window.plugin.tags.open(self.model())

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

    def openModel(self, model):

        self.setModel(model)
        self.model().itemChanged.connect(self.on_itemChanged)

        self.window.activateTabWidget(self)
        self.show()
        self.setFocus()

        self.watch()

    def actOnChoosen(self, model, index):
        if not self.isVisible(): return
        if index is None: return
        chosen=model.filePath(index)

        if self.chosenFor=='addWatchFolder':
            self.addWatchFolder(chosen)
        elif self.chosenFor=='addFolder':
            self.addFolder(chosen)

    def setModel(self, model):
        super().setModel(model)
        self.watch()

    def watch(self):

        return
        root=self.model().invisibleRootItem()

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
                self.addDocument(loc, item=wCon, recursively=True)

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
            self.delete(item)

    def addWatchFolder(self, path=False):
        if not self.isVisible(): return

        if not path:

            self.chosenFor='addWatchFolder'
            self.window.plugin.fileBrowser.toggle()

        else:

            self.chosenFor=None
            self.window.plugin.fileBrowser.toggle()

            wCon=None
            root=self.model().invisibleRootItem()
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

            self.setFocus()

    def deleteDocument(self):
        item=self.currentItem()
        if item is None: return
        if item.kind()!='document': return

        
        self.window.plugin.command.activateCustom(
                self._deleteDocument, 
                'Do you want to delete the document [yes/no]: ')

    def _deleteDocument(self, text):
        if text!='yes': return
        item=self.currentItem()
        if item is None: return
        if item.kind()!='document': return

        loc=self.window.plugin.tables.get('documents', {'id':item.id()}, 'loc')

        # from map
        self.delete(item)
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
        item=self.currentItem()
        if item is None or item.kind()!='document': return

        filePath=self.window.plugin.tables.get(
                'documents', {'id':item.id()}, 'loc')
        dirLoc=filePath.rsplit('/', 1)[0]

        self.window.plugin.command.activateCustom(
                self._moveDocumentTo, 'Move to: ', text=dirLoc)

    def _moveDocumentTo(self, text):
        item=self.currentItem()
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
        if parent is None: parent=self.model().invisibleRootItem()
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
                    self._addDocument(qIterator.next())
            else:
                self._addDocument(path)

            self.setFocus()

    def addDocument(self):
        if not self.isVisible(): return

        documents=self.window.plugin.tables.get('documents')
        data=[]
        titles=[]

        for d in documents:
            data+=[d]
            title=self.window.plugin.tables.get(
                    'metadata', {'did':d['id']}, 'title')
            if title is None: title=d['loc']
            titles+=[title]

        self.window.plugin.fuzzy.activate(
                self._addDocument, data, titles)

    def _addDocument(self, item):
        if item is None: return
        data=item.m_data

        newItem=Item('document', data['id'], self.window)
        currentItem=self.currentItem()

        if currentItem is None:
            parent=self.model().invisibleRootItem()
        else:
            parent=currentItem.parent()
            if parent is None:
                parent=self.model().invisibleRootItem()

        myDItem=self.isChild(newItem, parent)
        if myDItem is None:
            parent.appendRow(newItem)
            myDItem=newItem
        self.addAnnotations(myDItem)

    def updateMap(self, item=None):
        if item is None:
            item=self.model().invisibleRootItem()
        for index in range(item.rowCount()):
            self.updateMap(item.child(index))
        if item!=self.model().invisibleRootItem():
            if item.kind()!='container':
                r=self.window.plugin.tables.get(
                        item.kind(), {'id':item.id()}, 'id')
                if r is None:
                    parent=item.parent()
                    if parent is None: parent=self.model().invisibleRootItem()
                    parent.takeRow(item.row())
            if item.kind()=='document':
                self.addAnnotations(item)

    def updateTitles(self, sender):
        if sender==self: return
        self._updateTitles(sender=sender)

    def _updateTitles(self, item=None, sender=None):
        if not self.isVisible(): return
        if item is None:
            item=self.model().invisibleRootItem()
        for index in range(item.rowCount()):
            self._updateTitles(item.child(index), sender)
        if item!=self.model().invisibleRootItem():
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
            self.model().update()
        if item.m_changedFromOutside:
            item.m_changedFromOutside=False
        else:
            self.window.titleChanged.emit(self)

    def toggle(self):
        if not self.isVisible():
            if self.model() is None:
                self.openModel()
            self.window.activateTabWidget(self)
            self.setFocus()
        else:
            self.window.deactivateTabWidget(self)

    def close(self):
        self.window.deactivateTabWidget(self)

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
