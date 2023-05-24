from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from tables import Part as Table
from plugin import register, Item

from lura.utils import Plugin, register
from lura.utils import BaseInputListStack

class Part(Plugin):

    def __init__(self, app):

        super(Part, self).__init__(app, key='p')

        self.part=Table()
        
        self.setUI()

    def setUI(self):

        self.ui=BaseInputListStack(self, 'right', item_widget=Item)

        self.ui.main.input.hideLabel()
        self.ui.hideWanted.connect(self.deactivate)
        self.ui.main.returnPressed.connect(self.open)

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
        self.app.modes.setMode('plug')

        self.setData('abstract')
        self.ui.activate()

    @register('d')
    def deactivate(self):

        self.activated=False
        self.app.modes.setMode()
        self.ui.deactivate()

    @register('pr')
    def showReference(self): self.setData('reference')

    @register('pa')
    def showAbstract(self): self.setData('abstract')

    @register('po')
    def showOutline(self): self.setData('section')

    @register('pk')
    def showKeyword(self): self.setData('keyword')

    @register('ps')
    def showSummary(self): self.setData('summary')

    @register('pp')
    def showParagraph(self): self.setData('paragraph')

    @register('pb')
    def showBibliography(self): self.setData('bibliography')

    def setData(self, kind):

        if not self.activated: self.activate()

        view=self.app.window.display.currentView()
        if view: 
            dhash=view.document().hash() 
            data=self.part.search(f'hash:{dhash} kind:{kind}')
            for d in data:
                d['up']=d['text']
                d['up_color']='green'
            data=sorted(data, key=lambda x: (x['page'], x['y1']))
            self.ui.main.setList(data)

    @register('o')
    def open(self):

        item=self.ui.main.list.currentItem()
        if self.activated and item:
            page=item.itemData['page']+1
            y=item.itemData['y1']-0.05
            view=self.app.window.display.currentView()
            if view: view.jumpToPage(page, 0, y)
