from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from tables import Quickmark as Table
from lura.utils import Plugin, register
from plugin.widget import Item, InputList 

class Quickmark(Plugin):

    def __init__(self, app):

        super().__init__(app,
                         position='right',
                         mode_keys={'command': 't'},
                         bar_data={'edit':''},
                         listen_widget=[app.window],
                         exclude_widget=[app.window.bar.edit]
                         )

        self.marks = Table() 

        self.setUI()

        self.app.window.display.viewChanged.connect(self.setData)

    def setUI(self):

        super().setUI()

        main=InputList(item_widget=Item)

        self.ui.addWidget(main, 'main', main=True)
        self.ui.main.input.hideLabel()
        self.ui.main.returnPressed.connect(self.on_returnPressed)
        self.ui.main.inputTextChanged.connect(self.on_inputTextChanged)

        self.ui.hideWanted.connect(self.deactivateDisplay)
        self.ui.installEventFilter(self)

    def on_inputTextChanged(self):

        if self.ui.main.list.count()==1: self.on_returnPressed()

    def on_returnPressed(self):

        item=self.ui.main.list.currentItem()
        if item and 'position' in item.itemData:
            self.jump(item.itemData)
            self.ui.main.input.clear()
            self.deactivateDisplay()

    @register('dD')
    def deactivateDisplay(self):

        self.activated=False

        self.app.modes.setMode('normal')
        self.app.modes.plug.setClient()
        self.ui.deactivate()


    @register('d')
    def deactivate(self):

        if self.activated:

            self.activated=False

            self.app.modes.setMode('normal')
            self.app.modes.plug.setClient()

            self.app.window.bar.hide()

            self.app.window.bar.edit.textChanged.disconnect(self.write)
            self.app.window.bar.hideWanted.disconnect(self.deactivate)

    @register('a')
    def activate(self):

        view=self.app.window.display.currentView()
        if view:

            self.activated=True
            self.app.modes.plug.setClient(self)
            self.app.modes.setMode('plug')

            self.app.window.bar.show()
            self.app.window.bar.edit.setFocus()

            self.app.window.bar.hideWanted.connect(self.deactivate)
            self.app.window.bar.edit.textChanged.connect(self.write)

    @register('m', modes=['normal', 'command'])
    def mark(self): self.activate()

    @register('t', modes=['normal', 'command'])
    def goto(self): 

        self.activated=True
        self.app.modes.plug.setClient(self)
        self.app.modes.setMode('plug')
        self.ui.activate()

    def setData(self):

        document= self.app.window.display.view.document()
        if document:
            dhash = document.hash()
            rows=self.marks.getRow({'hash': dhash})
            for row in rows: row['up']=row['mark']
            if not rows: rows=[{'up': 'No quickmark is found'}]
            self.ui.main.setList(rows)

    @register('D')
    def delete(self):

        item=self.ui.main.list.currentItem()
        if self.activated and item: 
            self.marks.removeRow({'id': item.itemData['id']})
            self.setData()

    def write(self):

        mark=self.app.window.bar.edit.text()
        self.deactivate()

        if mark: 
            view = self.app.window.display.currentView()
            dhash= self.app.window.display.currentView().document().hash()
            page = self.app.window.display.currentView().currentPage()
            left, top = self.app.window.display.currentView().saveLeftAndTop()
            position=f'{page}:{left}:{top}'
            data={'hash':dhash, 'position': position, 'mark':mark}
            self.marks.writeRow(data)
            self.setData()

    def jump(self, mark):

        page, left, top = tuple(mark['position'].split(':'))
        self.app.window.display.currentView().jumpToPage(
                int(page), float(left), float(top))
        self.app.window.display.currentView().setFocus()
