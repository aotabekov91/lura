from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from collections import OrderedDict

from lura.render import PdfDocument
from lura.view import DocumentView

class BufferManager(QObject):

    documentCreated=pyqtSignal(object)
    documentRegistered=pyqtSignal(object)
    viewCreated=pyqtSignal(object)

    def __init__(self, app):
        super().__init__(app)
        self.app=app
        self.config=app.config
        self.views=[]
        self.documents={}

    def addView(self, filePath):
        document=self.loadDocument(filePath)
        if document:
            view=DocumentView(self.app, document)
            view.setId(len(self.views))
            self.views+=[view]
            self.viewCreated.emit(view)
            return view

    # def updateViews(self):
    #     for view in self.views:#.values():
    #         if view.isVisible(): view.readjust()

    def loadDocument(self, filePath):
        if filePath in self.documents:
            return self.documents[filePath]

        document=PdfDocument(filePath)
        if document.readSuccess():
            self.documents[filePath]=document

            self.documentCreated.emit(document)
            data=self.app.tables.get('documents', {'hash': document.hash()})

            if data is None:
                self.app.tables.write('documents', {'hash': document.hash(),
                                                    'path': filePath})
                data=self.app.tables.get('documents', {'hash':document.hash()})

            document.setParent(self.app)
            document.setId(data['id'])
            self.documentRegistered.emit(document)
            return document

    def getAllViews(self):
        return self.views

    def open(self, filePath):
        if filePath is None: return
        if type(filePath)!=list: filePath=[filePath,]
        for path in filePath:
            view=self.addView(path)
        return view

    def close(self, view):
        view.close()
        self.views.pop(view)

    def hideViews(self):
        [view.hide() for view in self.views]
