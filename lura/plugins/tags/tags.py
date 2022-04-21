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
        self.window.setTabLocation(self, self.location, self.name)
        self.setModel(QStandardItemModel())

    def showTagsFromTag(self, tagId):
        pass

    def showTagsFromModel(self, model):
        self.model().clear()

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
        model=self.model()

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

        self.model().appendRow(uContainer)

        self.window.activateTabWidget(self)

    def setItem(self, preList, itemDict, model):
        if len(preList)==1:
            if preList in itemDict:
                return itemDict[preList]
            else:
                tag=preList[0]
                item=QStandardItem(tag)
                model.appendRow(item)
                itemDict[preList]=item
            return item
        else:
            if preList in itemDict:
                return itemDict[preList]
            else:
                tag=preList[-1]
                item=QStandardItem(tag)
                preItem=self.setItem(preList[:-1], itemDict, model)
                preItem.appendRow(item)
                itemDict[preList]=item
                return item

    def getItem(self, rankedList, itemsDict, item):
        t=tuple(rankedList)
        if not t in itemsDict:
            newItem=QStandardItem(rankedList[-1])
            newItem.document=lambda: None
            itemsDict[t]=newItem
        else:
            newItem=itemsDict[t]

        newItem.appendRow(item)

        if len(rankedList)>1:
            self.getItem(rankedList[:-1], itemsDict, newItem)
        return newItem

       
    def _getTags(self, item, tagged=None, untagged=None, tags=None):
        if tagged is None:
            tagged={}
            untagged=[]
            tags=[]
        if hasattr(item, 'id') and item.kind()=='document':
            t=self.get(item.id(), item.kind())
            if len(t)>0:
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

    def get(self, m_id, kind='document'):
        return self.db.get(m_id, kind)

    def set(self, m_id, kind, tagList):
        self.db.set(m_id, kind, tagList)
