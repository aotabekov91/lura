#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.utils import Plugin
from lura.utils import watch

from tables import Bookmarks

class Bookmark(Plugin):

    def __init__(self, app):
        super().__init__(app)
        self.table=Bookmarks()

    @watch('display')
    def toggle(self):
        if not self.activated:
            self.activate()
        else:
            self.deactivate()

    def activate(self):
        statusbar=self.app.window.statusBar()
        self.activated=True
        statusbar.setClient(self)
        statusbar.setCommandInfo('Bookmark:')
        statusbar.commandEdit().returnPressed.connect(self.bookmark)
        statusbar.focusCommandEdit()

    def deactivate(self):
        if self.activated:
            self.activated=False
            statusbar=self.app.window.statusBar()
            statusbar.setClient()
            statusbar.clearCommand()
            statusbar.hide()
            statusbar.commandEdit().returnPressed.disconnect(self.bookmark)
            self.app.window.display.focusCurrentView()

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
            self.table.writeRow(data)
        self.deactivate()
