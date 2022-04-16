from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.plugins.tables import Table

class DatabaseConnector:

    def __init__(self, parent=None):
        self.m_parent=parent
        self.setup()

    def setup(self):
        self.m_parent.window.plugin.tables.addTable(AnnotationsTable)
        self.db = self.m_parent.window.plugin.tables.annotations

    def checkDocument(self, document):
        for ann in document.annotations():
            self.register(ann)

    def register(self, annotation):

        did = annotation.page().document().id()
        page = annotation.page().pageNumber()
        position=annotation.position()

        data = {'did': did, 'page': page, 'position': position}
        criteria=[{'field':k, 'value':v} for k,v in data.items()]

        aData=self.db.getRow(criteria)

        if len(aData)==0: 

            b=annotation.boundary()
            size=annotation.page().size()
            t=QTransform().scale(size.width(), size.height())
            topLeft=b.topLeft()
            bottomRight=b.bottomRight()
            b.setTopLeft(t.map(topLeft))
            b.setBottomRight(t.map(bottomRight))
            text=annotation.page().text(b)

            for f in ['"', '\n']:
                text=text.replace(f, ' ')

            data['content']=text
            data['color']=annotation.color()

            self.db.writeRow(data)
            aData=self.db.getRow(criteria)

        annotation.setId(aData[0]['id'])
        self.m_parent.window.annotationRegistered.emit(annotation)
        return annotation

class AnnotationsTable(Table):

    def __init__(self):

        self.fields = [
            'id integer PRIMARY KEY AUTOINCREMENT',
            'did int',
            'page int',
            'position text',
            'title text',
            'content text',
            'color text',
            'foreign key(did) references documents(id)',
            'constraint unique_ann unique (did, page, position)'
        ]
        super().__init__(table='annotations', fields=self.fields)
