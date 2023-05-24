from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin
from lura.utils import classify
from lura.utils import ListWidget

class Quickmark(Plugin):

    def __init__(self, app):
        super().__init__(app)

        self.marks = {}
        self.kind=None
        self.list=ListWidget(app, self, 'bottom', 'Quickmark')

    def deactivate(self):
        if self.activated:
            self.activated=False
            self.kind=None
            self.list.deactivate()
            statusbar=self.app.window.statusBar()
            statusbar.clearCommand()
            statusbar.keyPressEventOccurred.disconnect(self.keyPressEvent)
            statusbar.commandEdit().textChanged.disconnect(self.on_textChanged)
            statusbar.setClient()

    @classify(parent='display')
    def activate(self, kind='set'):
        statusbar=self.app.window.statusBar()
        if not self.activated:
            self.activated=True
            self.kind=kind
            statusbar.setClient(self)
            statusbar.setCommandInfo(f'Quickmark [{kind}]:')
            statusbar.commandEdit().textChanged.connect(self.on_textChanged)
            statusbar.keyPressEventOccurred.connect(self.keyPressEvent)
            statusbar.focusCommandEdit()
        else:
            self.deactivate()

    @classify(parent='display')
    def goto(self):
        view = self.app.window.display.currentView()
        dhash = view.document().hash()
        if dhash in self.marks:
            self.showList(dhash)
            self.activate(kind='jump')
        else:
            self.deactivate()

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape and self.activated:
            self.deactivate()

    def on_textChanged(self):
        statusbar=self.app.window.statusBar()
        mark=statusbar.commandEdit().text()
        if mark and self.kind=='set':
            self.set_mark(mark)
        elif self.activated and self.kind=='jump':
            self.goto_mark(mark)
        self.deactivate()

    def set_mark(self, mark):
        view = self.app.window.display.currentView()
        dhash= self.app.window.display.currentView().document().hash()
        page = self.app.window.display.currentView().currentPage()
        left, top = self.app.window.display.currentView().saveLeftAndTop()
        if not dhash in self.marks: self.marks[dhash] = {}
        self.marks[dhash][mark] = (page, left, top)

    def goto_mark(self, mark):
        view = self.app.window.display.currentView()
        dhash= self.app.window.display.currentView().document().hash()
        if mark in self.marks[dhash]:
            page, left, top = self.marks[dhash][mark]
            self.app.window.display.currentView().jumpToPage(page, left, top)
            self.app.window.display.currentView().setFocus()

    def showList(self, dhash):
        self.list.clear()
        data=[]
        for key, (page, top, left)  in self.marks[dhash].items():
            data+=[{'title': f'[{page}] {key}', 'content':False}]
        self.list.addItems(data)
        self.list.activate()
