from .. import Page
# from lura.render.pdf.model import PdfPlugin

from PyQt5.QtCore import *
from lura.core.widgets.tree import DocumentTreeWidget

class Document(QObject):

    annotationAdded=pyqtSignal(object)
    annotationRegistered=pyqtSignal(object)

    def __init__(self, filePath=None):
        super().__init__()
        self.m_shouldRegister=True
        self.m_registered=False
        self.m_data=None
        self.m_id=None
        self.m_annotations=[]
        self.m_filePath=filePath

    def widget(self):
        return DocumentTreeWidget(self)
    
    def removeAnnotation(self, annotation):
        annotation.toBeRemoved.emit(annotation)
        index=self.m_annotations.index(annotation)
        self.m_annotations.pop(index)
        annotation.page().removeAnnotation(annotation)

    def annotate(self, page, *args, **kwargs):
        annotation=page.annotate(*args, **kwargs)
        annotation.registered.connect(lambda: self.annotationRegistered.emit(self))
        self.m_annotations+=[annotation]

        return annotation

    def id(self):
        return self.m_id

    def isOnline(self):
        raise

    def setKind(self, kind):
        self.m_db.setKind(self, kind)

    def __eq__(self, other):
        return self.m_data==other.m_data

    def __hash__(self):
        return hash(self.m_data)
    
    def setDB(self, db):
        self.m_db=db

    def setTagDB(self, db):
        self.tagDB=db

    def tags(self):
        return self.tagDB.elementTags(self)

    def setTags(self, tags):
        self.tagDB.setElementTags(self, tags)

    def numberOfPages(self):
        return self.m_data.numberOfPages()

    def annotations(self):
        return self.m_annotations

    def setAnnotations(self):
        self.m_data.setAnnotations()

    def save(self, filePath, withChanges):
        return self.m_data.save(filePath, withChanges)

    def pages(self):
        return self.m_pages

    def setPages(self):
        return self.m_data.setPages()

    def search(self, text):
        return self.m_data.search(text)

    def loadOutline(self):
        return self.m_data.loadOutline()

    def page(self, index):
        return self.m_pages[index]

    def setId(self, did):
        self.m_id=did
        if did is not None: self.setRegistered(True)

    def data(self):
        return self.m_data

    def getField(self, fieldName):
        if fieldName=='kind':
            return 'document'
        elif fieldName=='filePath':
            return self.m_filePath
        return self.m_db.getField(fieldName, row_id_name='did', row_id_value=self.m_id)

    def setField(self, fieldName, fieldValue):
        self.m_db.setField(fieldName, fieldValue, row_id_name='did', row_id_value=self.m_id)

    def setFilePath(self, filePath):
        self.m_filePath = filePath

    def readSuccess(self):
        return self.m_data is not None

    def registered(self):
        return self.m_registered

    def setRegistered(self, condition):
        self.m_registered=condition

    def shouldRegister(self):
        return self.m_shouldRegister
