from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .table import BookmarksTable

class Bookmarks(QWidget):

    bookmarkDeleted=pyqtSignal(int)

    def __init__(self, parent, settings):
        super().__init__()
        self.window = parent 
        self.s_settings=settings
        self.name = 'bookmarks'
        self.globalKeys = {
                'Ctrl+b': (
                    self.addBookmark,
                    self.window,
                    Qt.WindowShortcut),
                }
        self.setup()
        
    def toggle(self):
        if not self.activated:
            self.window.activateStatusBar(self)
            self.activated=True
        else:
            self.window.deactivateStatusBar(self)
            self.activated=False

    def addBookmark(self, initial=True):

        if self.window.view() is None: return

        if initial:
            
            
            conditions=[{'field':'did', 'value': self.window.document().id()},
                    {'field':'page', 'value': self.window.view().currentPage()}, 
                    {'field':'position', 'value':'%f:%f'%self.window.view().saveLeftAndTop()}
                    ]
            bookmarks=self.db.getRow(conditions)

            if len(bookmarks)>0: self.lineEdit.setText(bookmarks[0]['text'])

            self.toggle()
            self.lineEdit.setFocus()

        else:

            self.toggle()

            data={'did': self.window.document().id(),
                    'page':self.window.view().currentPage(),
                    'text':self.lineEdit.text(),
                    'position':'%f:%f'%self.window.view().saveLeftAndTop()}

            self.register(data)

    def register(self, data):
        uniqueFields=['did', 'page', 'position']
        conditions=[{'field':f, 'value':data[f]} for f in uniqueFields]
        bookmark=self.db.getRow(conditions)
        if len(bookmark)>0: 
            return self.db.updateRow({'field':'id', 'value':bookmark[0]['id']}, data)
        self.db.writeRow(data)

    def setup(self):

        self.activated=False

        self.shortcuts={v:k for k, v in self.s_settings['shortcuts'].items()}

        self.window.plugin.tables.addTable(BookmarksTable)
        self.db=self.window.plugin.tables.bookmarks
        self.documentsDB=self.window.plugin.tables.documents

        self.label=QLabel('Bookmark')
        self.lineEdit=CQLineEdit()
        self.lineEdit.returnPressed.connect(lambda: self.addBookmark(initial=False))

        layout=QHBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.lineEdit)

    def keyPressEvent(self, event):
        key=event.text()
        if key in self.shortcuts:
            func=getattr(self, self.shortcuts[key])
            func()

class CQLineEdit(QLineEdit):

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.parent().toggle()
        else:
            super().keyPressEvent(event)
