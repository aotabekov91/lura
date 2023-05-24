#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.utils import Plugin
from lura.utils import classify

from tables import Bookmarks

class Bookmark(Plugin):

    def __init__(self, app):
        super().__init__(app)

        self.table=Bookmarks()

    @classify(parent='display', context=Qt.WidgetWithChildrenShortcut)
    def toggle(self):
        statusbar=self.app.window.statusBar()
        if not self.activated:
            self.activated=True
            statusbar.setClient(self)
            statusbar.setCommandInfo('Bookmark:')
            statusbar.commandEdit().returnPressed.connect(self.bookmark)
            statusbar.focusCommandEdit()
        else:
            self.deactivate()

    @classify(parent='display')
    def deactivate(self):
        if self.activated:
            self.activated=False
            statusbar=self.app.window.statusBar()
            statusbar.setClient()
            statusbar.clearCommand()
            statusbar.commandEdit().returnPressed.disconnect(self.bookmark)
            self.app.window.display.currentView().setFocus()

    def bookmark(self):
        view=self.app.window.display.currentView()
        statusbar=self.app.window.statusBar()
        if view:
            data={}
            data['position']=':'.join([str(f) for f in view.saveLeftAndTop()])
            data['page']=view.pageItem().page().pageNumber()
            data['text']=statusbar.commandEdit().text()
            data['dhash']=view.document().hash()
            data['kind']='document'
            data['source']=view.document().filePath()
            print(data)
            self.table.writeRow(data)
        self.deactivate()
