from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin.widget import Item
from tables import Quickmark as Table

from lura.utils import watch, Plugin
from lura.utils import BaseInputListStack

class Quickmark(Plugin):

    def __init__(self, app):

        super().__init__(app)

        self.marks = Table() 
        self.setUI()

        self.app.window.display.viewChanged.connect(self.setData)

    def setUI(self):

        self.ui=BaseInputListStack(self, 'bottom', item_widget=Item)

        self.ui.main.input.hideLabel()
        self.ui.hideWanted.connect(self.ui.deactivate)

        self.ui.main.returnPressed.connect(self.on_returnPressed)
        self.ui.main.inputTextChanged.connect(self.on_inputTextChanged)

        self.ui.installEventFilter(self)

    def on_inputTextChanged(self):

        if self.ui.main.list.count()==1: self.on_returnPressed()

    def on_returnPressed(self):

        item=self.ui.main.list.currentItem()
        if item and 'position' in item.itemData:
            self.jump(item.itemData)
            self.ui.main.input.clear()
            self.ui.deactivate()

    def deactivate(self):

        bar=self.app.window.bar
        bar.edit.textChanged.disconnect(self.write)
        bar.edit.clear()
        bar.info.setText('')
        bar.info.hide()
        bar.edit.hide()
        bar.hide()

    def activate(self):

        bar=self.app.window.bar

        bar.info.setText(f'Quickmark:')
        bar.edit.textChanged.connect(self.write)

        bar.show()
        bar.info.show()
        bar.edit.show()
        bar.edit.setFocus()

    @watch('display')
    def mark(self): 

        self.activate()

    @watch('display')
    def goto(self): self.ui.activate()

    def setData(self):

        document= self.app.window.display.view.document()
        if document:
            dhash = document.hash()
            rows=self.marks.getRow({'hash': dhash})
            for row in rows: row['up']=row['mark']
            if not rows: rows=[{'up': 'No quickmark is found'}]
            self.ui.main.setList(rows)

    def delete(self):

        item=self.ui.main.list.currentItem()
        if item: 
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
