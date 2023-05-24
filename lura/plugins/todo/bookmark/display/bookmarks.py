import os
import functools

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin
from lura.utils import watch, key
from lura.utils import getPosition, getBoundaries

from lura.utils.widgets import InputListEdit

class Bookmarks(Plugin):

    def __init__(self, app):
        super(Bookmarks, self).__init__(app)

        self.list=InputListEdit(app, self, 'right', 'Bookmarks')
        self.list.contentChanged.connect(self.on_contentChanged)
        self.list.listReturnPressed.connect(self.on_returnPressed)
        self.list.inputReturnPressed.connect(self.on_returnPressed)
        self.list.installEventFilter(self)

    def on_returnPressed(self):
        item=self.list.currentItem()
        dhash=item.itemData['dhash']
        page=item.itemData['page']
        x, y=(float(i) for i in item.itemData['position'].split(':'))
        data=self.app.tables.hash.getRow({'hash': dhash})
        print(data, item.itemData)
        for f in data:
            print(f)
            if os.path.exists(f['path']):
                self.app.window.open(f['path'], how='reset')
                view=self.app.window.display.currentView()
                if view:
                    view.jumpToPage(page, x, y-0.4)
                    return self.list.input.setFocus()

    def on_contentChanged(self, widget):
        data=widget.data
        bid=data['id']
        text=widget.textDown()
        self.app.tables.update('bookmarks', {'id':bid}, {'text':text})

    @key('o')
    def open(self):
        self.on_returnPressed()
        self.app.window.display.setFocus()

    @key('d')
    def remove(self):
        item=self.list.currentItem()
        nrow=self.list.currentRow()-1
        bid=item.itemData['id']
        self.app.tables.bookmarks.removeRow({'id':bid})
        self.setData()
        self.list.setCurrentRow(nrow)
        self.list.input.setFocus()

    @watch('window', Qt.WidgetWithChildrenShortcut)
    def toggle(self):
        if not self.activated:
            self.activate()
        else:
            self.deactivate()
                
    def activate(self):
        self.activated=True
        self.activateStatusbar()
        self.setData()
        self.list.activate()
        self.list.input.setFocus()

    @key('u')
    def setData(self):
        bookmarks={}
        criteria={}
        view=self.app.window.display.currentView()
        if view:
            criteria['dhash']=view.document().hash()
            bookmarks = self.app.tables.bookmarks.getRow(criteria)
            if bookmarks:
                for a in bookmarks:
                    a['up']=f'# {a.get("id")}'
                    a['down']=a['text']
            self.list.setList(bookmarks)

    @key('q')
    def deactivate(self):
        self.activated=False
        self.deactivateStatusbar()
        self.list.deactivate()
