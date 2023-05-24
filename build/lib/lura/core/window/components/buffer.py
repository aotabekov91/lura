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
            data=self.app.tables.hash.getRow({'hash': document.hash()})
            if data is None:
                self.app.tables.hash.writeRow({'hash': document.hash()})
                data=self.app.tables.hash.getRow({'hash': document.hash()})
            document.setParent(self.app)
            document.setId(data['id'])
            self.documentCreated.emit(document)
            return document
