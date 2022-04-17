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

        self.itemDoubleClicked.connect(self.jump)
        self.window.viewChanged.connect(self.on_viewChanged)
        self.window.setTabLocation(self, self.location, self.name)

    def find(self):
        view=self.window.view()
        if view is None or type(view.document())!=PdfDocument: return
        self.window.plugin.command.activateCustom(self.search, 'Search: ')

    def paintMatches(self, painter, options, widget, pageItem):

        if self.currentMatch is None: return
        if self.currentPage!=pageItem.page().pageNumber(): return
        if hasattr(painter, 'r') and painter.r==self.currentMatch: return

        painter.setPen(QPen(Qt.red, 0.0))
        painter.drawRect(self.currentMatch)
        painter.r=self.currentMatch

    def search(self, text):
        
        self.matches=[]
        self.currentMatch=None
        self.currentIndex=-1

        if text == '': return

        self.window.activateTabWidget(self)

        self.window.view().updateSceneAndView()

        self.matches=search(text, self.window.view().document())

        if len(self.matches) == 0: return

        self.clear()
        for i, (pageNumber, rectF) in enumerate(self.matches):

            pageItem=self.window.view().pageItem(pageNumber-1)
            text=self.getFullLineText(pageItem, rectF)
            item=QListWidgetItem()

            itemRectF=pageItem.mapToItem(rectF)[0]


            item.setText(text)

            item.m_pageNumber=pageNumber
            item.m_rectF=itemRectF

            self.addItem(item)

        self.window.view().pageHasBeenJustPainted.connect(self.paintMatches)
        self.jump('next')
        self.setFocus()
        
    def jump(self, data):

        if len(self.matches)==0: return

        if type(data)==str:

            if data=='next':
                self.currentIndex+=1
                if self.currentIndex>=len(self.matches):
                    self.currentIndex=0

            elif data=='prev':
                self.currentIndex-=1
                if self.currentIndex<0:
                    self.currentIndex=len(self.matches)-1

            self.currentPage=self.matches[self.currentIndex][0]
            pageItem=self.window.view().pageItem(self.currentPage-1)
            currentMatch=self.matches[self.currentIndex][1]
            self.currentMatch=pageItem.mapToItem(currentMatch)[0]

        else:

            self.currentPage=data.m_pageNumber
            pageItem=self.window.view().pageItem(self.currentPage-1)
            self.currentMatch=data.m_rectF

        self.window.view().jumpToPage(self.currentPage)
        sceneRect=pageItem.mapRectToScene(self.currentMatch)
        self.window.view().centerOn(0, sceneRect.y())
        self.setFocus()

    def getFullLineText(self, pageItem, rectF):
        width=pageItem.page().size().width()
        lineRectF=QRectF(0, rectF.y(), width, rectF.height())
        return pageItem.page().text(lineRectF)

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
