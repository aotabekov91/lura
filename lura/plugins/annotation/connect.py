from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.render import createAnnotation
from .table import AnnotationsTable

class DatabaseConnector:

    def __init__(self, parent=None):
        self.m_parent=parent
        self.colorSystem = parent.s_settings['colorSystem']
        self.setup()

    def setup(self, aTable=None, dTable=None):
        if aTable is None:
            self.m_parent.window.plugin.tables.addTable(AnnotationsTable)
            self.db = self.m_parent.window.plugin.tables.annotations
        else:
            self.db=aTable

    def get(self, aid):

        aData=self.db.getRow({'field':'id', 'value':aid})
        if len(aData)==0: return
        aData=aData[0]

        if self.m_parent is not None:

            document=self.m_parent.window.plugin.documents.get(aData['did'])
            if document is None: return

            if not document.isOnline(): 
                annotation=createAnnotation(kind='pdf')
                annotation.setPage(document.page(aData['page']-1))
            else:
                annotation=createAnnotation(kind='web')
                annotation.setPage(document)
            annotation.setDB(self)
            annotation.setId(aid)
            self.m_parent.window.annotationRegistered.emit(annotation)

            return annotation

    def data(self, annotation):
        data=self.db.getRow({'field':'id', 'value':annotation.id()})
        if len(data)==0: return
        return dict(data[0])

    def getBy(self, condition):
        return [self.get(a['id']) for a in self.db.getRow(condition)]

    def getAll(self, did):
        return self.db.getRow({'field':'did', 'value':did})

    def title(self, annotation):
        data=self.db.getRow({'field':'id', 'value':annotation.id()})
        if len(data)==0: return
        return data[0]['title']

    def setTitle(self, annotation, title):
        self.db.updateRow({'field':'id', 'value':annotation.id()}, {'title':title})

    def color(self, annotation):
        data=self.db.getRow({'field':'id', 'value':annotation.id()})
        if len(data)==0: return
        return data[0]['color']

    def setColor(self, annotation, color):
        self.db.updateRow({'field':'id', 'value':annotation.id()}, {'color':color})

    def content(self, annotation):
        data=self.db.getRow({'field':'id', 'value':annotation.id()})
        if len(data)==0: return
        return data[0]['content']
    
    def setContent(self, annotation, content):
        self.db.updateRow({'field':'id', 'value':annotation.id()}, {'content':content})

    def position(self, annotation):
        data=self.db.getRow({'field':'id', 'value':annotation.id()})
        if len(data)==0: return
        return data[0]['position']

    def quote(self, annotation):
        data=self.db.getRow({'field':'id', 'value':annotation.id()})
        if len(data)==0: return
        return data[0]['quote']
    
    def setQuote(self, annotation, quote):
        self.db.updateRow({'field':'id', 'value':annotation.id()}, {'quote':quote})
        if annotation.content() in ['', None, 'None']:
            self.setContent(annotation, quote) 

    def setPosition(self, annotation, position):
        self.db.updateRow({'field':'id', 'value':annotation.id()}, {'position':position})

    def getKind(self, annotation):
        for kind, colorHex in self.colorSystem.items():
            if QColor(colorHex)== annotation.color(): return kind
        return ''

    def populateFields(self, annotation):

        if annotation.title() in ['None', None]: 
            self.setTitle(annotation, '')
        if annotation.content() in ['', 'None', None]: 
            quote=annotation.quote()
            if not quote in ['', None]: self.setContent(annotation, quote)
        if annotation.color() in ['', 'None', None]:
            self.setColor(annotation, QColor('white').name())

    def register(self, annotation):

        annotation.setDB(self)

        did = annotation.page().document().id()
        page = annotation.page().pageNumber()
        position=annotation.getPosition()

        data = {'did': did, 'page': page, 'position': position}
        criteria=[{'field':k, 'value':v} for k,v in data.items()]

        aData=self.db.getRow(criteria)

        if len(aData)==0: 
            self.db.writeRow(data)
            aData=self.db.getRow(criteria)

        annotation.setId(aData[0]['id'])
        self.populateFields(annotation)
        self.m_parent.window.annotationRegistered.emit(annotation)
        return annotation
