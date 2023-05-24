import re

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
        self.db = self.m_parent.window.plugin.tables

    def register(self, annotation, boundary=None):

        did = annotation.page().document().id()
        page = annotation.page().pageNumber()
        position=annotation.position()

        cond = {'did': did, 'page': page, 'position': position}

        aid=self.db.get('annotations', cond, 'id') 

        if aid is None: 

            data=cond.copy()

            content=[]

            size=annotation.page().size()
            t=QTransform().scale(size.width(), size.height())
            if type(boundary)!=list: boundary=[boundary]

            for b in boundary: 

                if b is None: continue

                x=.99*b.topLeft().x()
                topLeft=QPointF(x, b.topLeft().y())

                x=1.01*b.bottomRight().x()
                bottomRight=QPointF(x, b.bottomRight().y())

                b.setTopLeft(t.map(topLeft))
                b.setBottomRight(t.map(bottomRight))

                content+=[annotation.page().text(b)]

            if len(content)>0:
                text=' '.join(content)
                text=re.sub(re.compile(r'  *'), ' ', text)
                data['content']=text

            data['color']=annotation.color()

            self.db.write('annotations', data)
            aid=self.db.get('annotations', data, 'id')

        annotation.setId(aid)

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
