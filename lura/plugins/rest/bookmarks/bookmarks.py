from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .table import BookmarksTable

from lura.core.miscel import MapTree

from lura.core.miscel import Item
from lura.core.miscel import ItemModel

class Bookmarks(MapTree):

    bookmarkChanged=pyqtSignal()

    def __init__(self, parent, settings):
        super().__init__(parent, parent)
        self.window = parent
        self.s_settings=settings
        self.location='right'
        self.name = 'bookmarks'
        self.globalKeys = {
                'Ctrl+b': (
                    self.addBookmark,
                    self.window,
                    Qt.WindowShortcut),
                'Ctrl+Shift+b': (
                    self.toggle,
                    self.window,
                    Qt.WindowShortcut),
                }
        self.setup()

    def setup(self):

        self.bookmarkChanged.connect(self.update)
        self.window.plugin.tables.addTable(BookmarksTable)
        self.window.setTabLocation(self, self.location, self.name)
        
    def toggle(self):
        if not self.isVisible():
            self.showBookmakrs()
        else:
            self.window.deactivateTabWidget(self)

    def showBookmakrs(self, view=None):
        if view is None: view=self.window.view()
        if view is None: return

        model=ItemModel()
        self.setModel(model)

        condition={'did':self.window.document().id()}

        bookmarks=self.window.plugin.tables.get('bookmarks', condition,
                unique=False)

        if bookmarks is None or len(bookmarks)==0: return

        model.itemChanged.connect(self.on_itemChanged)
        for b in bookmarks:
            item=Item('bookmark', b['id'], self.window, b['text'])
            model.appendRow(item)

        self.window.activateTabWidget(self)
        self.setFocus()

    def open(self):
        item=self.currentItem()
        if item is None: return

        print(item.id(), type(item.id()))
        data=self.window.plugin.tables.get('bookmarks', {'id':item.id()})
        if data is None: return
        filePath=self.window.plugin.tables.get(
                'documents', {'id':data['did']}, 'loc')

        position=data['position'].split(':')
        left, top=float(position[0]), float(position[1])

        self.window.open(filePath)
        self.window.view().jumpToPage(data['page'], left, top)
        self.window.view().setFocus()

    def delete(self):
        item=self.currentItem()
        if item is None: return

        self.window.plugin.tables.remove('bookmarks', {'id':item.id()})
        self.bookmarkChanged.emit()
        self.setFocus()

    def update(self):
        if not self.isVisible(): return
        self.showBookmakrs()

    def addBookmark(self):

        if self.window.view() is None: return

        conditions={'did':self.window.document().id(),
                'page': self.window.view().currentPage(),
                'position' :'%f:%f'%self.window.view().saveLeftAndTop()}

        text=self.window.plugin.tables.get(
                'bookmarks', conditions, 'text')

        if text is None: text=''

        self.window.plugin.command.activateCustom(
                self._addBookmark, 'Bookmark: ', None, text)

    def _addBookmark(self, text):

        data={'did': self.window.document().id(),
                'page':self.window.view().currentPage(),
                'text': text,
                'position':'%f:%f'%self.window.view().saveLeftAndTop()}

        self.register(data)
        self.bookmarkChanged.emit()

    def register(self, data):
        uniqueFields=['did', 'page', 'position']
        conditions={f:data[f] for f in uniqueFields}
        bookmark=self.window.plugin.tables.get(
                'bookmarks', conditions)
        if bookmark is not None:
            self.window.plugin.tables.update(
                    'bookmarks', conditions, {'text':data['text']})
        else:
            self.window.plugin.tables.write('bookmarks', data)

    def on_itemChanged(self, item):
        self.window.plugin.tables.update(
                'bookmarks', {'id':item.id()}, {'text':item.text()})

    def close(self):
        self.window.deactivateTabWidget(self)
