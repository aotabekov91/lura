from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from collections import OrderedDict

from lura.render.pdf import PdfDocument
from lura.view.docviewer import DocumentView

class BufferManager(QObject):

    def __init__(self, parent, configuration):
        super().__init__(parent)
        self.window=parent
        self.configuration=configuration
        self.views=OrderedDict()

    def addView(self, filePath):

        if filePath in self.views: return self.views[filePath]

        document=self.loadDocument(filePath)
        if document is None: return 

        view=DocumentView(self.window, self.configuration.copy())
        view.open(document)

        self.views[filePath]=view
        return view

    def updateViews(self):
        for view in self.views.values():
            if view.isVisible(): view.readjust()

    def loadDocument(self, filePath):
        
        document=PdfDocument(filePath)
        if document is None or not document.readSuccess(): return

        document.setParent(self.window)
        self.window.documentCreated.emit(document)
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
