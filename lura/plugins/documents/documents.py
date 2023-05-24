from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin import UpDown, InputList
from lura.utils import Plugin, register

class Documents(Plugin):

    def __init__(self, app):

        super().__init__(app, position='right', mode_keys={'command': 'd'})

        self.setUI()
        self.ui.main.setList(self.getList())

    def setUI(self):

        super().setUI()

        main=InputList(item_widget=UpDown)
        self.ui.addWidget(main, 'main', main=True)

        self.ui.main.input.hideLabel()
        self.ui.main.returnPressed.connect(self.on_returnPressed)
        self.ui.hideWanted.connect(self.deactivate)
        self.ui.installEventFilter(self)

    @register('a')
    def activate(self):

        self.activated=True
        self.app.modes.plug.setClient(self)
        self.app.modes.setMode('plug')
        self.ui.activate()

    @register('d')
    def deactivate(self):

        self.activated=False
        self.app.modes.setMode('normal')
        self.ui.deactivate()

    @register('t')
    def toggle(self):

        if self.activated:
            self.deactivate()
        else:
            self.activate()

    def getList(self):

        data=self.app.tables.hash.getAll()
        for d in data:
            d['up']=d['path'].split('/')[-1]
            meta=self.app.tables.metadata.getRow({'hash':d['hash']})
            if meta and meta[0]['title']:
                d['down']=meta[0]['title']
                d['up']=d['path'].split('/')[-1]
                d['up_color']='green'
        return data

    def on_returnPressed(self): 

        self.open(focus=False)
        self.ui.show()

    @register('o')
    def open(self, focus=True, how='reset', hide=False):

        if self.activated:

            if hide: self.deactivate()
            if not focus or hide: self.deactivateCommandMode()

            item=self.ui.main.list.currentItem()
            if item:
                path=self.app.tables.hash.getPath(item.itemData['hash'])
                if path: self.app.window.open(path, how=how)

    @register('O')
    def openAndHide(self): 

        if self.activated: self.open(focus=True, hide=True)

    @register('i')
    def openBelow(self): 

        if self.activated: self.open(focus=True, how='below')

    @register('I')
    def openBelowAndHide(self): 

        if self.activated: self.open(how='below', hide=True)
