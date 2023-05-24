from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from tables import Part as Table
from plugin import register, UpDown

from lura.utils import watch, Plugin
from lura.utils import BaseInputListStack

class Part(Plugin):

    def __init__(self, app):

        super(Part, self).__init__(app)

        self.part=Table()
        self.setUI()

    def setUI(self):

        self.ui=BaseInputListStack(self, 'right', item_widget=UpDown)

        self.ui.main.input.hideLabel()
        self.ui.main.returnPressed.connect(self.on_returnPressed)
        self.ui.hideWanted.connect(self.deactivate)

        self.ui.installEventFilter(self)

    @watch('display', Qt.WidgetWithChildrenShortcut)
    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()
                
    def activate(self):

        self.activated=True
        self.setData('abstract')
        self.ui.activate()

    def deactivate(self):

        self.activated=False
        self.ui.deactivate()

    @register('r')
    def showReference(self): self.setData('reference')

    @register('a')
    def showAbstract(self): self.setData('abstract')

    @register('o')
    def showOutline(self): self.setData('section')

    @register('k')
    def showKeyword(self): self.setData('keyword')

    @register('s')
    def showSummary(self): self.setData('summary')

    @register('p')
    def showParagraph(self): self.setData('paragraph')

    @register('b')
    def showBibliography(self): self.setData('bibliography')

    def setData(self, kind):

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

    def on_returnPressed(self):

        item=self.ui.main.list.currentItem()
        if item:
            raise
            page=0
            x, y = 0, 0
            view=self.app.window.display.currentView()
            if view: view.jumpToPage(page, x, y)
