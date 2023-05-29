from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from tables import Part as Table
from plugin import Item, InputList
from lura.utils import Plugin, register

from .widget import PartTree

class Part(Plugin):

    def __init__(self, app):

        super(Part, self).__init__(app, position='right', mode_keys={'command': 'p'})

        self.app.main.display.viewChanged.connect(self.update)

        self.part=Table()
        self.setUI()

    def setUI(self):

        super().setUI()

        tree=PartTree()
        self.ui.addWidget(tree, 'tree')

        main=InputList(item_widget=Item)
        self.ui.addWidget(main, 'main', main=True)
        self.ui.main.input.hideLabel()
        self.ui.main.returnPressed.connect(self.open)

        self.ui.hideWanted.connect(self.deactivate)
        self.ui.installEventFilter(self)

    @register('tr')
    def toggleTree(self):

        if self.ui.tree.isVisible():
            self.ui.show()
        else:
            self.ui.show(self.ui.tree)

    def update(self, view):

        dhash=view.document().hash()
        data=self.part.getTreeDict(dhash)
        if data: self.ui.tree.installData({'root': data})

    @register('t', modes=['command'])
    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()
                
    def activate(self):

        self.activated=True
        self.ui.activate()
        self.toggleTree()

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

        view=self.app.main.display.currentView()
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
            view=self.app.main.display.currentView()
            if view: view.jumpToPage(page, 0, y)
