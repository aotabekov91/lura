from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from tables import Part as Table
from plugin import register, UpDown

from lura.utils import Plugin
from lura.utils import BaseInputListStack

class Part(Plugin):

    def __init__(self, app):

        super(Part, self).__init__(app, key='p')

        self.part=Table()
        self.setUI()

    def setUI(self):

        self.ui=BaseInputListStack(self, 'right', item_widget=UpDown)

        self.ui.main.input.hideLabel()
        self.ui.main.returnPressed.connect(self.open)
        self.ui.hideWanted.connect(self.deactivate)

        self.ui.installEventFilter(self)

    @register('t')
    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()
                
    @register('a')
    def activate(self):

        self.activated=True
        self.setData('abstract')
        self.ui.activate()

    @register('d')
    def deactivate(self):

        self.activated=False
        self.ui.deactivate()

    @register('sr')
    def showReference(self): self.setData('reference')

    @register('sa')
    def showAbstract(self): self.setData('abstract')

    @register('so')
    def showOutline(self): self.setData('section')

    @register('sk')
    def showKeyword(self): self.setData('keyword')

    @register('ss')
    def showSummary(self): self.setData('summary')

    @register('sp')
    def showParagraph(self): self.setData('paragraph')

    @register('sb')
    def showBibliography(self): self.setData('bibliography')

    def setData(self, kind):

        if not self.activated: self.activate()

        view=self.app.window.display.currentView()
        if view: 
            dhash=view.document().hash() 
            dlist=[]
            data=self.part.search(f'hash:{dhash} kind:{kind}')
            for d in data:
                name=d['hash']
                if d['title']: name=d['title']
                dlist+=[{'up': name, 'down': d['text'], 'id':d['hash'], 'data':d, 'up_color': 'green'}]
            self.ui.main.setList(dlist)

    @register('o')
    def open(self):

        item=self.ui.main.list.currentItem()
        if self.activated and item:
            raise
            page=0
            x, y = 0, 0
            view=self.app.window.display.currentView()
            if view: view.jumpToPage(page, x, y)
