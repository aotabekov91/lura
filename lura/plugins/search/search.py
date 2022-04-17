#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.render.pdf import PdfDocument

def search(text, document):
    found=[]
    for page in document.pages():
        matches=page.search(text)
        for m in matches:
            found+=[(page.pageNumber(), m)]
    return found

class Search(QListWidget):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent
        self.s_settings=settings
        self.name = 'search'
        self.location='bottom'
        self.globalKeys= {
                '/': (
                    self.find,
                    self.window,
                    Qt.WindowShortcut)
                }
        self.setup()

    def setup(self):
        nextAction=QShortcut('n', self)
        nextAction.setContext(Qt.WidgetShortcut)
        nextAction.activated.connect(lambda: self.jump('next'))
        prevAction=QShortcut('p', self)
        prevAction.setContext(Qt.WidgetShortcut)
        prevAction.activated.connect(lambda: self.jump('prev'))

        self.itemDoubleClicked.connect(self.on_doubleClicked)
        self.window.viewChanged.connect(self.on_viewChanged)
        self.window.setTabLocation(self, self.location, self.name)

    def find(self):
        view=self.window.view()
        if view is None or type(view.document())!=PdfDocument: return 
        self.window.plugin.command.activateCustom(self.search, 'Search: ')

    def paintMatches(self, painter, options, widget, pageItem):

        if self.currentMatch is None: return
        painter.setPen(QPen(Qt.red, 0.0))
        painter.drawRect(self.currentMatch)

    def search(self, text):
        
        self.matches=[]
        self.currentMatch=None
        self.currentIndex=-1

        if text == '': return

        self.matches=search(text, self.window.view().document())

        if len(self.matches) == 0: return 

        self.clear()
        for i, (pageNumber, rectF) in enumerate(self.matches):
            text=str(pageNumber)
            item=QListWidgetItem(text)
            item.setData(0, pageNumber)
            item.setData(1, rectF)
            self.addItem(item)
        self.window.activateTabWidget(self)

        self.window.view().pageHasBeenJustPainted.connect(self.paintMatches)
        self.jump('next')
        self.setFocus()
        
    def jump(self, kind):

        if len(self.matches)==0: return

        if kind=='next':
            self.currentIndex+=1
            if self.currentIndex>=len(self.matches):
                self.currentIndex=0

        elif kind=='prev':
            self.currentIndex-=1
            if self.currentIndex<0:
                self.currentIndex=len(self.matches)-1

        pageNumber=self.matches[self.currentIndex][0]
        pageItem=self.window.view().pageItem(pageNumber-1)
        currentMatch=self.matches[self.currentIndex][1]
        self.currentMatch=pageItem.mapToItem(currentMatch)[0]
        self.window.view().jumpToPage(pageNumber)
        self.setFocus()

    def on_doubleClicked(self, item):
        if len(self.matches)==0: return
        pageNumber=int(item.data(0))
        currentMatch=item.data(1)
        print(pageNumber, currentMatch)
        pageItem=self.window.view().pageItem(pageNumber-1)
        self.currentMatch=pageItem.mapToItem(currentMatch)[0]
        self.window.view().jumpToPage(pageNumber)
        self.setFocus()

    def on_viewChanged(self, view):
        if not hasattr(self, 'matches'): return
        self.window.deactivateTabWidget(self)
        self.clear()
        self.matches=[]
        self.currentMatch=None

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.window.deactivateTabWidget(self)
            self.window.view().setFocus()
