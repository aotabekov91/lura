from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin.widget import Item

from lura.utils import Plugin, watch
from lura.utils import BaseInputListStack

class Search(Plugin):

    def __init__(self, app):

        super(Search, self).__init__(app=app)

        self.match=None
        self.show_statusbar=False

        self.app.window.display.installEventFilter(self)

        self.setUI()

    def setUI(self):
        
        self.ui=BaseInputListStack(self, 'bottom', item_widget=Item)

        self.ui.main.input.hide()
        self.ui.main.input.hideLabel()
        self.ui.hideWanted.connect(self.deactivate)

        self.ui.main.list.currentItemChanged.connect(self.on_itemChanged)

        self.ui.installEventFilter(self)

    def on_itemChanged(self, item): 

        if item: self.jump(match=item.itemData)

    def activate(self):

        if not self.activated:

            self.activated=True
            self.autolisten=True

            bar=self.app.window.bar
            bar.hideWanted.connect(self.deactivate)
            bar.edit.returnPressed.connect(self.find)

            bar.show()
            bar.edit.show()
            bar.info.show()
            bar.info.setText('Search:')

            bar.edit.setFocus()

            if self.app.window.display.view:
                self.app.window.display.view.pageHasBeenJustPainted.connect(self.paint)

    def deactivate(self):

        if self.activated:
            
            self.activated=False
            self.autolisten=False

            self.clear()

            bar=self.app.window.bar

            bar.hide()
            bar.clear()
            bar.info.hide()
            bar.info.setText('')
            bar.edit.hide()

            bar.edit.returnPressed.disconnect(self.find)
            bar.hideWanted.disconnect(self.deactivate)

            self.ui.deactivate()

            if self.app.window.display.view:
                self.app.window.display.view.setFocus()
                self.app.window.display.view.pageHasBeenJustPainted.disconnect(self.paint)

    def clear(self):

        self.matches=[]
        self.index=-1
        self.match=None

    def find(self):

        def search(text, view, found=[]):

            if view:
                document=view.document()
                for page in document.pages().values():
                    rects=page.search(text)
                    for rect in rects:
                        line=self.getLine(text, page, rect)
                        found+=[{'page': page.pageNumber(), 'rect': rect, 'up': line}]
            return found

        text=self.app.window.bar.edit.text()

        self.clear()

        if text:
            self.matches=search(text, self.app.window.display.view)
            if len(self.matches) > 0: 
                self.ui.main.setList(self.matches)
                self.ui.main.list.setCurrentRow(0)

    def toggleList(self):

        if self.ui.isVisible():
            self.ui.deactivate()
        else:
            if len(self.matches)>0: 
                self.ui.activate()
                self.ui.main.setFocus()
        
    def jump(self, increment=1, match=None):

        if len(self.matches)==0: return

        if not match:

            self.index+=increment
            if self.index>=len(self.matches):
                self.index=0
            elif self.index<0:
                self.index=len(self.matches)-1

            match=self.matches[self.index]
            self.ui.main.list.setCurrentRow(self.index)
        
        page=match['page']
        rect=match['rect']

        pageItem=self.app.window.display.view.pageItem(page-1)
        self.match=pageItem.mapToItem(rect)[0]
        sceneRect=pageItem.mapRectToScene(self.match)

        self.app.window.display.view.jumpToPage(page)
        self.app.window.display.view.centerOn(0, sceneRect.y())

    def next(self): self.jump(+1)

    def prev(self): self.jump(-1)

    def focusSearch(self): self.app.window.statusBar().edit.setFocus()

    def getLine(self, text, page, rectF):

        width=page.size().width()
        lineRectF=QRectF(0, rectF.y(), width, rectF.height())
        line=f'<html>{page.find(lineRectF)}</html>'
        replacement=f'<font color="red">{text}</font>'
        return line.replace(text, replacement)
        
    def paint(self, painter, options, widget, pageItem):

        if self.match:
            if hasattr(painter, 'r') and painter.r==self.match: return
            painter.setPen(QPen(Qt.red, 0.0))
            painter.drawRect(self.match)
            painter.r=self.match
