from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .table import *

class DatabaseConnector:
    def __init__(self, parent=None):
        self.m_parent=parent
        if parent is not None: 
            self.setup()
        else:
            self.setup(standAlone=True)

    def setup(self, standAlone=False):
        if not standAlone:
            self.m_parent.window.plugin.tables.addTable(TagsTable)
            self.m_parent.window.plugin.tables.addTable(TaggedTable)
            self.m_tags = self.m_parent.window.plugin.tables.tags
            self.m_tagged = self.m_parent.window.plugin.tables.tagged

        else:
            self.m_tags=TagsTable()
            self.m_tagged=TaggedTable()

    def getTagged(self, tag):
        tagData=self.m_tags.getRow({'field':'tag', 'value':tag})
        if len(tagData)>0:
            return self.m_tagged.getRow({'field': 'tid', 'value': tagData[0]['id']})

    def get(self, uid, kind):
        tids=self.m_tagged.getRow([{'field':'uid', 'value':uid},
            {'field':'kind', 'value':kind}])
        tags=[]
        for tid in [t['tid'] for t in tids]:
            tags+=[self.m_tags.getRow({'field':'id', 'value':tid})[0]['tag']]
        return '; '.join(tags)

    def register(self, tag):
        data=self.m_tags.getRow({'field':'tag', 'value':tag})
        if len(data)==0: self.m_tags.writeRow({'tag':tag})
        return self.m_tags.getRow({'field':'tag', 'value':tag})[0]['id']

    def tag(self, uid, kind, tag):
        tid=self.register(tag)
        self.m_tagged.writeRow({'tid':tid, 'uid':uid, 'kind':kind})

    def setTags(self, uid, kind, tags):
        condition= [{'field':'uid', 'value':uid}, {'field':'kind', 'value':kind}]
        self.m_tagged.removeRow(condition)
        if '::' in tags:
            tags=[f.strip() for f in tags.split('::')]
        elif ';' in tags:
            tags=[f.strip() for f in tags.split(';')]
        else:
            tags=[tags]
        for tag in tags:
            if tag!='': self.tag(uid, kind, tag)

    def elementTags(self, element):
        return self.get(element.id(), element.getField('kind')+'s')

    def setElementTags(self, element, tags):
        self.setTags(element.id(), element.getField('kind')+'s', tags)
        self.cleanUp()

    def cleanUp(self):
        tagged=set([f['tid'] for f in self.m_tagged.getAll()])
        tags=[f['id'] for f in self.m_tags.getAll()]
        toBeDeleted=tags.copy()
        for tid in tags:
            if tid in tagged: toBeDeleted.pop(toBeDeleted.index(tid))
        for tid in toBeDeleted:
            self.m_tags.removeRow({'field':'id', 'value':tid})

