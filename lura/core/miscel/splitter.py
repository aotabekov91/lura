from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class DisplaySplitter(QSplitter):

    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):

        self.leftSP=QSplitter(Qt.Vertical, self)
        self.left=QVBoxLayout(self.leftSP)
        self.left.setContentsMargins(0,0,0,0)
        self.left.setSpacing(0)

        self.centerSP=QSplitter(Qt.Vertical, self)
        self.center=QVBoxLayout(self.centerSP)
        self.center.setContentsMargins(0,0,0,0)
        self.center.setSpacing(0)

        self.rightSP=QSplitter(Qt.Vertical, self)
        self.right=QVBoxLayout(self.rightSP)
        self.right.setContentsMargins(0,0,0,0)
        self.right.setSpacing(0)

    def clear(self, layout):
        for index in range(layout.count()):
            item=layout.takeAt(index)
            item.widget().hide()

    def setWidget(self, widget):
        if widget.__class__.__name__=='MapView':
            self.clear(self.left)
            self.left.addWidget(widget)
        elif widget.__class__.__name__=='DocumentView':
            self.clear(self.center)
            self.center.addWidget(widget)
        elif widget.__class__.__name__=='BrowserView':
            self.clear(self.right)
            self.right.addWidget(widget)

    def removeWidget(self, widget):
        if widget.__class__.__name__=='MapView':
            self.clear(self.left)
            self.left.removeWidget(widget)
        elif widget.__class__.__name__=='DocumentView':
            self.clear(self.center)
            self.center.removeWidget(widget)
        elif widget.__class__.__name__=='BrowserView':
            self.clear(self.right)
            self.right.removeWidget(widget)

    def addWidget(self, widget):
        if widget.__class__.__name__=='MapView':
            self.left.addWidget(widget)
        elif widget.__class__.__name__=='DocumentView':
            self.center.addWidget(widget)
        elif widget.__class__.__name__=='BrowserView':
            self.right.addWidget(widget)

    def replaceWidget(self, index, widget):
        if widget.__class__.__name__=='DocumentView':
            if self.center.count()>0: 
                self.center.insertWidget(index, widget)
                self.center.takeAt(index+1)
            else:
                self.center.addWidget(widget)
        elif widget.__class__.__name__=='BrowserView':
            if self.right.count()>0: 
                self.right.insertWidget(index, widget)
                self.right.takeAt(index+1)
            else:
                self.right.addWidget(widget)
        elif widget.__class__.__name__=='MapView':
            if self.left.count()>0: 
                self.left.insertWidget(index, widget)
                self.left.takeAt(index+1)
            else:
                self.left.addWidget(widget)

    def focusMapView(self):
        self.leftSP.show()
        if self.left.count()>0: self.left.itemAt(0).widget().setFocus()

    def focusDocumentView(self):
        self.centerSP.show()
        if self.center.count()>0: self.center.itemAt(0).widget().setFocus()

    def focusBrowserView(self):
        self.rightSP.show()
        if self.right.count()>0: self.right.itemAt(0).widget().setFocus()

    def onlyMapView(self):
        self.leftSP.show()
        self.centerSP.hide()
        self.rightSP.hide()

    def onlyDocumentView(self):
        self.centerSP.show()
        self.leftSP.hide()
        self.rightSP.hide()

    def onlyBrowserView(self):
        self.leftSP.hide()
        self.centerSP.hide()
        self.rightSP.show()
