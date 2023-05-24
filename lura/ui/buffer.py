from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.render import PdfDocument

class Buffer(QObject):

    documentCreated=pyqtSignal(object)

    def __init__(self, app):
        super().__init__()

        self.app=app
        self.documents={}

    def loadDocument(self, filePath):
        if filePath in self.documents:
            return self.documents[filePath]
        document=PdfDocument(filePath)
        if document.readSuccess():
            self.documents[filePath]=document
            did=self.app.tables.index.id(filePath)
            dhash=self.app.tables.index.hash(filePath)
            if did:
                document.setParent(self.app)
                document.setHash(dhash)
                document.setId(did)
                self.documentCreated.emit(document)
                return document
