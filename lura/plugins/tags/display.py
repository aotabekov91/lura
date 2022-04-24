from collections import Counter

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.core.miscel import *

class TagView(MapTree):

    def __init__(self, parent, window):
        super().__init__(window, window)
        self.m_parent=parent
        self.window = window
        self.location='left'
        self.name='tagview'

        self.setup()

    def setup(self):

        self.m_mainModel=None
        self.tagItems=None

        self.currentItemChanged.connect(self.window.mapItemChanged)
        self.window.setTabLocation(self, self.location, self.name)

    def rootUp(self):
        if self.m_mainModel is None: return
        self.openModel(self.m_mainModel)

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
        if item is None: return True
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

        model=ItemModel()

        for k, v in self.tagItems.items():
            if not tag in k: continue

            for kk in v:
                ii=Item(kk.kind(), kk.id(), self.window, kk.text())
                model.invisibleRootItem().appendRow(ii)

        self.openModel(model)

    def getModel(self):

        allTagged=self.window.plugin.tables.get('tagged')

        model=ItemModel()

        for t in allTagged:
            item=Item(t['kind'], t['uid'], self.window)
            model.appendRow(item)

        return model

    def openModel(self, model=None):

        if model is None: model=self.getModel()

        tagsDict, untagged, allTags=self._getTags(model.invisibleRootItem())

        tagCountDict=dict(Counter(allTags))

        tagItems={}

        for item, tags in tagsDict.items():
            itemTagsRanked=sorted(tags, key=lambda t: tagCountDict[t], reverse=True)
            itemTagsRanked=tuple(itemTagsRanked)

            if itemTagsRanked in tagItems:
                tagItems[itemTagsRanked]+=[item]

            else:
                tagItems[itemTagsRanked]=[item]

        sortedKeys=sorted(tagItems.keys(), key=lambda k: len(k))

        itemDict={}

        model=ItemModel()
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
        if hasattr(item, 'id'):
            t=self.m_parent.get(item.id(), item.kind())
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
