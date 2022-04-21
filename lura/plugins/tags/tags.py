from collections import Counter

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.core import Item
from lura.core import MapTree
from lura.view.docviewer import DocumentView

from .connect import DatabaseConnector

class Tags(MapTree):

    def __init__(self, parent, settings):
        self.name = 'tags'
        self.location='left'
        self.window = parent
        self.s_settings = settings
        self.db = DatabaseConnector(self) 

        self.globalKeys = {
            'Ctrl+t': (
                self.tag,
                self.window,
                Qt.WindowShortcut)
        }

        super().__init__(parent, parent)
        self.setup()

    def setup(self):
        super().setup()

        self.m_mainModel=None
        self.tagItems=None

        self.open=self.openNode
        self.window.setTabLocation(self, self.location, self.name)
        self.currentItemChanged.connect(
                self.window.mapItemChanged)

    def showTagsFromTag(self, tagId):
        pass

    def rootUp(self):
        if self.m_mainModel is None: return
        self.showTagsFromModel(self.m_mainModel)

    def getParentTags(self, item, ancesstors):
        parent=item.parent()
        if parent is None: return
        ancesstors+=[parent.text()]
        self.getParentTags(parent, ancesstors)

    def setModel(self, model):
        super().setModel(model)
        model.itemChanged.connect(self.itemChanged)

    def edit(self, index, *args, **kwargs):
        item=self.currentItem()
        if item.kind()!='container': return True
        self.oldTag=item.text()
        return super().edit(index, *args, **kwargs)

    def itemChanged(self, item):
        if item.kind()!='container': return

        newTag=item.text()

        for k, v in self.tagItems.items():
            if not self.oldTag in k: continue
            tags=[]
            for t in k:
                if t!=self.oldTag: tags+=[t]
            tags+=[newTag]
            for vv in v:
                self.set(vv.id(), vv.kind(), tags)

        self.oldTag=None
        self.rootUp()

    def delete(self):
        item=self.currentItem()
        if item is None: return
        if item.kind()!='container': return

        tag=item.text()

        for k, v in self.tagItems.items():
            if not tag in k: continue
            for vv in v:
                self.untag(vv.kind(), vv.id(), tag)

        self.rootUp()

    def makeRoot(self):
        item=self.currentItem()
        if item is None: return
        if item.kind()!='container': return

        tag=item.text()

        model=QStandardItemModel()

        for k, v in self.tagItems.items():
            if not tag in k: continue

            for kk in v:
                ii=Item(kk.kind(), kk.id(), self.window, kk.text())
                model.invisibleRootItem().appendRow(ii)

        self.showTagsFromModel(model)

    def showTagsFromModel(self, model):

        if model is None: return

        tagsDict, untagged, allTags=self._getTags(model.invisibleRootItem())

        tagCountDict=dict(Counter(allTags))

        tagItems={}

        for item, tags in tagsDict.items():
            itemTagsRanked=sorted(
                    tags, key=lambda t: tagCountDict[t], reverse=True)
            itemTagsRanked=tuple(itemTagsRanked)

            if itemTagsRanked in tagItems:
                tagItems[itemTagsRanked]+=[item]

            else:
                tagItems[itemTagsRanked]=[item]

        sortedKeys=sorted(tagItems.keys(), key=lambda k: len(k))

        itemDict={}

        model=QStandardItemModel()
        if self.m_mainModel is None: 
            self.m_mainModel=model
            self.tagItems=tagItems

        for k in sortedKeys:
            self.setItem(k, itemDict, model)

        for k, v in tagItems.items():
            for item in v:
                i=Item(item.kind(), item.id(), self.window)
                itemDict[k].appendRow(i)

        uContainer=Item('container', None, self.window, 'untagged')

        for item in untagged:
            i=Item(item.kind(), item.id(), self.window)
            uContainer.appendRow(i)

        if model==self.m_mainModel:
            model.appendRow(uContainer)

        self.setModel(model)
        self.window.activateTabWidget(self)
        self.setFocus()

    def setItem(self, preList, itemDict, model):
        if preList in itemDict:
            return itemDict[preList]
        else:
            tag=preList[-1]
            item=Item('container', None, self.window, tag)
            if len(preList)==1:
                model.appendRow(item)
            else:
                preItem=self.setItem(preList[:-1], itemDict, model)
                preItem.appendRow(item)
            itemDict[preList]=item
            return item

    def _getTags(self, item, tagged=None, untagged=None, tags=None):
        if tagged is None:
            tagged={}
            untagged=[]
            tags=[]
        if hasattr(item, 'id') and item.kind()=='document':
            t=self.get(item.id(), item.kind())
            if len(t)>0:
                t=sorted(t)
                tagged[item]=t
                tags+=t
            else:
                untagged+=[item]
        for i in range(item.rowCount()):
            child=item.child(i)
            self._getTags(child, tagged, untagged, tags)
        return tagged, untagged, tags

    def tag(self):
        if type(self.window.view())==DocumentView:
            m_id=self.window.view().document().id()
            tags=self.get(m_id, 'document')
        else:
            document=self.window.view().tree()
            item=document.currentItem()
            if item is None: return
            m_id=item.id()
            kind=item.kind()
            tags=self.get(m_id, kind)

        text='; '.join(tags)
        self.window.plugin.command.activateCustom(
                self._tag, 'Tag: ', text=text)

    def _tag(self, text):
        if type(self.window.view())==DocumentView:
            document=self.window.view().document()
            m_id=document.id()
            kind='document'
        else:
            document=self.window.view().tree()
            item=document.currentItem()
            if item is None: return
            m_id=item.id()
            kind=item.kind()

        tags=[a.strip() for a in text.split(';')]
        self.set(m_id, kind, tags)

        self.window.documentTagged.emit(m_id, kind, tags, self)
        self.window.view().setFocus()

    def openNode(self):
        item = self.currentItem()
        if item is None: return
        if item.kind() != 'document': return

        filePath = self.window.plugin.tables.get(
            'documents', {'id': item.id()}, 'loc')
        self.window.open(filePath)

        self.setFocus()

    def get(self, m_id, kind='document'):
        return self.db.get(m_id, kind)

    def set(self, m_id, kind, tagList):
        self.db.set(m_id, kind, tagList)

    def untag(self, kind, m_id, tag):
        self.db.untag(kind, m_id, tag)

    def close(self):
        self.window.deactivateTabWidget(self)
