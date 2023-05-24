import os
import threading

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin.utils import register
from plugin.widget import UpDownEdit, InputList

from lura.utils import Plugin, watch
from lura.utils import getPosition, getBoundaries, BaseInputListStack

class BookmarkDisplayer(Plugin):

    def __init__(self, app):

        super(BookmarkDisplayer, self).__init__(app)

        self.bookmarks=[]
        self.app.window.display.viewChanged.connect(self.updateData)

        self.setUI()

    def setUI(self):

        self.ui=BaseInputListStack(self, 'right', item_widget=UpDownEdit) 

        self.ui.main.input.hideLabel()
        self.ui.hideWanted.connect(self.deactivate)
        self.ui.main.returnPressed.connect(self.on_returnPressed)
        self.ui.main.list.widgetDataChanged.connect(self.on_contentChanged)

        self.ui.installEventFilter(self)

    def on_returnPressed(self):

        item=self.ui.main.list.currentItem()
        dhash=item.itemData['hash']
        page=item.itemData['page']
        x, y=(float(i) for i in item.itemData['position'].split(':'))
        data=self.app.tables.hash.getPath(dhash)

        view=self.app.window.display.currentView()
        if view and view.document():
            if dhash!=view.document().hash():
                path=self.app.tables.hash.getPath(dhash)
                if os.path.exists(path): self.app.window.open(path, how='reset')

        view=self.app.window.display.currentView()
        if view: view.jumpToPage(page, x, y-0.4)

        return self.ui.show()

    def on_contentChanged(self, widget):

        bid=widget.data['id']
        text=widget.data['down']
        self.app.tables.bookmark.updateRow({'id':bid}, {'text':text})

    @register('o')
    def open(self):

        self.on_returnPressed()
        self.app.window.display.setFocus()

    @register('d')
    def remove(self):

        item=self.ui.main.list.currentItem()
        nrow=self.ui.main.list.currentRow()-1
        bid=item.itemData['id']
        self.app.tables.bookmark.removeRow({'id':bid})
        self.updateData()
        self.ui.main.list.setCurrentRow(nrow)
        self.ui.show()

    @register('u')
    def updateData(self, view=None):

        if not view: view=self.app.window.display.currentView()

        if view:
            criteria={'hash': view.document().hash()}
            self.bookmarks = self.app.tables.bookmark.getRow(criteria)
            if self.bookmarks:
                for a in self.bookmarks:
                    a['up']=f'# {a.get("id")}'
                    a['down']=a['text']
            self.ui.main.setList(self.bookmarks)

    def activate(self):

        self.activated=True
        self.ui.activate()

    def deactivate(self):

        self.activated=False
        self.ui.deactivate()

    @register('s', command=True)
    def toggle(self): super().toggle()
