#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.utils import Plugin

def search(text, document):
    found=[]
    for page in document.pages():
        matches=page.search(text)
        for m in matches:
            found+=[(page.pageNumber(), m)]
    return found

class Search(Plugin):

    def __init__(self, app):
        super(Search, self).__init__(app)
        self.currentMatch=None

    def activate(self):
        statusbar=self.app.window.statusBar()
        if not self.activated:
            self.activated=True
            self.app.window.keyPressEventOccurred.connect(self.keyPressEvent)
            self.app.window.view().pageHasBeenJustPainted.connect(self.paintMatches)
            statusbar.setClient(self)
            statusbar.setCommandInfo('[Search]')
            statusbar.commandEdit().returnPressed.connect(self.search)
            statusbar.keyPressEventOccurred.connect(self.keyPressEvent)
            statusbar.focusCommandEdit()
        else:
            statusbar.toggle()

    def deactivate(self):
        if self.activated:
            self.activated=False
            self.app.window.keyPressEventOccurred.disconnect(self.keyPressEvent)
            self.app.window.view().pageHasBeenJustPainted.disconnect(self.paintMatches)
            statusbar=self.app.window.statusBar()
            statusbar.setClient()
            statusbar.clearCommand()
            statusbar.commandEdit().returnPressed.disconnect(self.search)

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.deactivate()
        elif self.activated and event.text() in self.actions:
            self.actions[event.text()]()

    def search(self):
        statusbar=self.app.window.statusBar()
        text=statusbar.commandEdit().text()

        self.matches=[]
        self.currentMatch=None
        self.currentIndex=-1

        if text == '': return

        self.matches=search(text, self.app.window.view().document())

        if len(self.matches) > 0: self.jump(1)
        
    def jump(self, increment):
        if len(self.matches)==0: return

        self.currentIndex+=increment
        if self.currentIndex>=len(self.matches):
            self.currentIndex=0
        elif self.currentIndex<0:
            self.currentIndex=len(self.matches)-1

        pageNumber, currentMatch=self.matches[self.currentIndex]
        pageItem=self.app.window.view().pageItem(pageNumber-1)
        self.currentMatch=pageItem.mapToItem(currentMatch)[0]

        self.app.window.view().jumpToPage(pageNumber)
        sceneRect=pageItem.mapRectToScene(self.currentMatch)
        self.app.window.view().centerOn(0, sceneRect.y())
        self.app.window.setFocus()

    def searchNext(self):
        self.jump(+1)

    def searchPrev(self):
        self.jump(-1)

    def focusSearch(self):
        self.app.window.statusBar().commandEdit().setFocus()

    def getFullLineText(self, pageItem, rectF):
        width=pageItem.page().size().width()
        lineRectF=QRectF(0, rectF.y(), width, rectF.height())
        return pageItem.page().text(lineRectF)

    def paintMatches(self, painter, options, widget, pageItem):
        if self.currentMatch is None: return
        if hasattr(painter, 'r') and painter.r==self.currentMatch: return
        painter.setPen(QPen(Qt.red, 0.0))
        painter.drawRect(self.currentMatch)
        painter.r=self.currentMatch
