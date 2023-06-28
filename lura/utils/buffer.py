import os

from plugin.app import Buffer
from ..render import PdfDocument

class LuraBuffer(Buffer):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.documents={}

    def load(self, filePath):

        filePath=os.path.abspath(filePath)

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
                self.bufferCreated.emit(document)
                return document
