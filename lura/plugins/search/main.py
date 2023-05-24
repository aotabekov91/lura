from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin import ListWidget
from plugin.widget import Item

from lura.utils import Plugin, BaseCommandStack, register

class Search(Plugin):

    def __init__(self, app):

        super(Search, self).__init__(
                app=app, 
                name='search', 
                position='bottom',
                bar_data={'edit':''},
                mode_keys={'command':'s'},
                listen_widget=[app.window],
                exclude_widget=[app.window.bar.edit],
                )

        self.index=-1
        self.matches=[]
        self.match=None

        self.setUI()

    def setUI(self):
        
        super().setUI()

        self.listen_widget+=[self.ui]
        main=ListWidget(item_widget=Item, check_fields=['up'])

        self.ui.focusGained.connect(self.setFocus)
        self.ui.addWidget(main, 'main', main=True)
        self.ui.installEventFilter(self)

    @register('l', modes=['command', 'search'])
    def toggleList(self):

        if self.ui.isVisible():
            self.ui.deactivate()
        else:
            self.ui.activate()
            self.app.window.setFocus()

    @register('n', modes=['command', 'search'])
    def next(self): self.jump(+1)

    @register('p', modes=['command', 'search'])
    def prev(self): self.jump(-1)

    @register('f', modes=['command', 'search'])
    def focusSearch(self): self.app.window.statusBar().edit.setFocus()

    @register('/', modes=['normal', 'command', 'search'])
    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()

    @register('a')
    def activate(self):

        view=self.app.window.display.currentView()

        if view:

            self.activated=True
            self.listening=True

            self.app.modes.plug.setClient(self)
            self.app.modes.plug.delistenWanted.connect(self.deactivate)

            self.app.modes.setMode('plug')

            self.app.window.bar.edit.setFocus()
            self.app.window.bar.edit.returnPressed.connect(self.find)

            self.app.window.bar.hideWanted.connect(self.deactivate)

    @register('d')
    def deactivate(self):

        if self.activated:
            
            self.activated=False
            self.listening=False

            self.clear()
            self.ui.deactivate()

            self.app.modes.plug.setClient()
            self.app.modes.plug.delistenWanted.disconnect(self.deactivate)

            self.app.modes.setMode('normal')

            self.app.window.bar.edit.returnPressed.disconnect(self.find)

    def clear(self):

        self.index=-1
        self.match=None
        self.matches=[]

    def find(self):

        def search(text, view, found=[]):
            if view:
                document=view.document()
                for page in document.pages().values():
                    rects=page.search(text)
                    if rects:
                        for rect in rects:
                            line=self.getLine(text, page, rect)
                            found+=[{'page': page.pageNumber(), 'rect': rect, 'up': line}]
            return found

        text=self.app.window.bar.edit.text()

        self.clear()

        self.app.window.setFocus()

        if text:
            self.matches=search(text, self.app.window.display.view)
            if len(self.matches) > 0: 
                self.ui.main.setList(self.matches)
                self.jump()
            else:
                self.ui.main.setList([{'up': f'No match found for {text}'}])

    def jump(self, increment=1, match=None):

        if len(self.matches)==0: return

        if not match:

            self.index+=increment
            if self.index>=len(self.matches):
                self.index=0
            elif self.index<0:
                self.index=len(self.matches)-1

            match=self.matches[self.index]
            self.ui.main.setCurrentRow(self.index)
        
        page=match['page']
        rect=match['rect']

        pageItem=self.app.window.display.view.pageItem(page-1)
        matchMapped=pageItem.mapToItem(rect)
        pageItem.setSearched([matchMapped])
        sceneRect=pageItem.mapRectToScene(matchMapped)

        self.app.window.display.view.jumpToPage(page)
        self.app.window.display.view.centerOn(0, sceneRect.y())

    def getLine(self, text, page, rectF):

        width=page.size().width()
        lineRectF=QRectF(0, rectF.y(), width, rectF.height())
        line=f'<html>{page.find(lineRectF)}</html>'
        replacement=f'<font color="red">{text}</font>'
        return line.replace(text, replacement)
