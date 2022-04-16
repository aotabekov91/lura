from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from collections import OrderedDict

from lura.render import loadDocument as load

from lura.view.mapviewer import MapView
# from lura.view.webviewer import BrowserView
from lura.view.docviewer import DocumentView

class BufferManager(QObject):

    def __init__(self, parent, configuration):
        super().__init__(parent)
        self.window=parent
        self.configuration=configuration
        self.views=OrderedDict()
        self.documents=OrderedDict()

    def addView(self, filePath):

        if filePath in self.views: return self.views[filePath]

        if filePath in self.documents:
            document=self.documents[filePath]
        else:
            document=self.loadDocument(filePath)
        
        if document is None: return 

        # if document.__class__.__name__=='WebDocument':
            # view=BrowserView(self.window, self.configuration.copy())
        if document.__class__.__name__ in ['PdfDocument']:
            view=DocumentView(self.window, self.configuration.copy())
        elif document.__class__.__name__=='MapDocument':
            view=MapView(self.window, self.configuration.copy())

        view.open(document)
        self.views[filePath]=view
        return self.views[filePath]

    def updateViews(self):
        for view in self.views.values():
            if view.isVisible(): view.readjust()

    def loadDocument(self, filePath):
        
        if filePath in self.documents: return self.documents[filePath]

        document=load(filePath)
        if document is not None and document.readSuccess():
            document.setParent(self.window)

            if document.__class__.__name__ in ['PdfDocument', 'WebDocument']: 
                self.window.documentCreated.emit(document)
            elif document.__class__.__name__ in ['MapDocument']: 
                self.window.mapCreated.emit(document)

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
        if not filePath in self.documents: return
        self.documents.pop(filePath)
        if not filePath in self.views: return
        view=self.views.pop(filePath)
        view.close()

    def hideViews(self):
        [view.hide() for view in self.views.values()]
