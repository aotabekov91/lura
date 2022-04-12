from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.render import createAnnotation
from .table import AnnotationsTable

class DatabaseConnector:

    def __init__(self, parent=None):
        self.m_parent=parent
        self.setup()

    def setup(self):
        self.m_parent.window.plugin.tables.addTable(AnnotationsTable)
        self.db = self.m_parent.window.plugin.tables.annotations

    def get(self, did=None, aid=None):
        if did is not None:
            return self.db.getRow({'field':'did', 'value':did})
        if aid is not None:
            return self.db.getRow({'field':'aid', 'value':aid})[0]

    def register(self, annotation):

        annotation.setDB(self.db)

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
        self.m_parent.window.annotationRegistered.emit(annotation)
        return annotation
