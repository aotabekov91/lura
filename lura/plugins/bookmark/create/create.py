from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin import register
from lura.utils import Plugin

class BookmarkCreator(Plugin):

    def activate(self):

        self.activated=True
        bar=self.app.window.statusBar()
        bar.info.setText('Bookmark:')
        bar.edit.returnPressed.connect(self.bookmark)
        bar.show()
        bar.info.show()
        bar.edit.show()
        bar.edit.setFocus()

    def deactivate(self):

        self.activated=False
        bar=self.app.window.statusBar()
        bar.edit.clear()
        bar.info.hide()
        bar.edit.hide()
        bar.hide()
        bar.edit.returnPressed.disconnect(self.bookmark)
        self.app.window.display.focusCurrentView()

    def bookmark(self):

        bar=self.app.window.statusBar()
        view=self.app.window.display.currentView()
        if view:
            data={}
            data['kind']='document'
            data['text']=bar.edit.text()
            data['hash']=view.document().hash()
            data['page']=view.pageItem().page().pageNumber()
            data['position']=':'.join([str(f) for f in view.saveLeftAndTop()])

            self.app.tables.bookmark.writeRow(data)

    @register('a', command=True)
    def toggle(self): super().toggle()

