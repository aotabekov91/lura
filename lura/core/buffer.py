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
            dhash=self.app.tables.hash.hash(filePath)
            if dhash:
                document.setParent(self.app)
                document.setHash(dhash)
                document.setId(dhash)
                self.documentCreated.emit(document)
                return document
