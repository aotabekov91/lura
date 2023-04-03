from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from collections import OrderedDict

from lura.render import PdfDocument
from lura.view import DocumentView

class BufferManager(QObject):

    documentCreated=pyqtSignal(object)
    documentRegistered=pyqtSignal(object)

    def __init__(self, app):
        super().__init__(app)
        self.app=app
        self.config=app.config
        self.views=OrderedDict()
        self.documents={}

    def addView(self, filePath):

        if filePath in self.views: return self.views[filePath]

        document=self.loadDocument(filePath)
        if document is None: return 

        view=DocumentView(self.app, document)

        self.views[filePath]=view
        return view

    def updateViews(self):
        for view in self.views.values():
            if view.isVisible(): view.readjust()

    def loadDocument(self, filePath):
        
        if filePath in self.documents:
            return self.documents[filePath]

        document=PdfDocument(filePath)
        if document.readSuccess():

            self.documentCreated.emit(document)
            data=self.app.tables.get('documents', {'loc':filePath})

            if data is None:

                self.app.tables.write('documents', {'loc': filePath})
                data=self.app.tables.get('documents', {'loc':filePath})

            document.setParent(self.app)
            document.setId(data['id'])
            self.documentRegistered.emit(document)

            return document

    def getAllViews(self):
        return list(self.views.values())

    def getView(self, filePath=None): 
        if filePath is None and len(self.views)>0: return self.views[list(self.views.keys())[-1]]
        if filePath in self.views: return self.views[filePath]

    def open(self, filePath):

        if filePath is None: return
        if filePath in self.views: return self.views[filePath]
        if type(filePath)!=list: filePath=[filePath,]
        [self.addView(path) for path in filePath]
        return self.views.get(filePath[-1], None)

    def close(self, filePath):
        if not filePath in self.views: return
        return self.views.pop(filePath)

    def hideViews(self):
        [view.hide() for view in self.views.values()]
