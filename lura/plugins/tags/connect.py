from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.plugins.tables import Table

class DatabaseConnector:
    def __init__(self, parent=None):
        self.window=parent.window
        self.m_parent=parent
        self.setup()

    def setup(self):
        self.m_parent.window.plugin.tables.addTable(TagsTable)
        self.m_parent.window.plugin.tables.addTable(TaggedTable)

    def get(self, uid, kind):
        tids=self.window.plugin.tables.get(
                'tagged', {'uid':uid, 'kind':kind}, 'tid', unique=False)

        tags=[]
        for tid in tids:
            tags+=self.window.plugin.tables.get(
                    'tags', {'id':tid}, 'tag', unique=False)
        return tags

    def set(self, uid, kind, tags):

        self.window.plugin.tables.remove('tagged', {'uid':uid})

        for tag in tags:
            if tag=='': continue

            tid=self.window.plugin.tables.get('tags', {'tag':tag}, 'id')
            if tid is None:
                self.window.plugin.tables.write('tags', {'tag':tag})
                tid=self.window.plugin.tables.get('tags', {'tag':tag}, 'id')

            self.window.plugin.tables.write(
                    'tagged', {'tid':tid, 'uid':uid, 'kind':kind})

        self.cleanUp()

    def cleanUp(self):
        allTagged=self.window.plugin.tables.get('tagged')
        allTags=self.window.plugin.tables.get('tags')

        taggedIds=set([t['tid'] for t in allTagged])
        tagIds=[t['id'] for t in allTags]

        toBeDeleted=tagIds.copy()
        for tid in tagIds:
            if tid in taggedIds: toBeDeleted.pop(toBeDeleted.index(tid))

        for tid in toBeDeleted:
            self.window.plugin.tables.remove('tags', {'id':tid})


class TaggedTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'tid int',
            'uid int',
            'kind text',
            'foreign key(tid) references tags(id)',
            'constraint unique_tagged unique (tid, uid, kind)',
        ]

        super().__init__(table='tagged', fields=self.fields)


class TagsTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'tag text',
        ]
        super().__init__(table='tags', fields=self.fields)
