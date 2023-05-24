from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin
from lura.utils.widgets import ListWidget
from lura.render import PdfDocument

class Quickmark(Plugin):

    def __init__(self, app):
        super().__init__(app, 'quickmark')

        self.marks = {}
        self.kind=None
        self.list=ListWidget(app, self, 'bottom', 'quickmark')

    def deactivate(self):
        if self.activated:
            self.activated=False
            self.kind=None
            statusbar=self.app.window.statusBar()
            statusbar.setClient()
            statusbar.clearCommand()
            statusbar.commandEdit().textChanged.disconnect(self.on_textChanged)

    def activate(self, kind='set'):
        statusbar=self.app.window.statusBar()
        if not self.activated:
            self.activated=True
            self.kind=kind
            statusbar.setClient(self)
            statusbar.setCommandInfo(f'Quickmark [{kind}]:')
            statusbar.commandEdit().textChanged.connect(self.on_textChanged)
            statusbar.focusCommandEdit()
        else:
            self.deactivate()

    def on_textChanged(self):
        statusbar=self.app.window.statusBar()
        mark=statusbar.commandEdit().text()
        if mark and self.kind=='set':
            self.set_mark(mark)
        elif self.activated and self.kind=='jump':
            self.goto_mark(mark)
            self.list.deactivate()
        self.deactivate()

    def set_mark(self, mark):
        view = self.app.window.view()
        did = self.app.window.view().document().id()
        page = self.app.window.view().currentPage()
        left, top = self.app.window.view().saveLeftAndTop()
        if not did in self.marks: self.marks[did] = {}
        self.marks[did][mark] = (page, left, top)

    def goto_mark(self, mark):
        view = self.app.window.view()
        did = self.app.window.view().document().id()
        if mark in self.marks[did]:
            page, left, top = self.marks[did][mark]
            self.app.window.view().jumpToPage(page, left, top)
            self.app.window.view().setFocus()

    def goto(self):
        view = self.app.window.view()
        did = view.document().id()
        if did in self.marks:
            self.showList(did)
            self.activate(kind='jump')
        else:
            self.deactivate()

    def showList(self, did):
        self.list.clear()
        for mark in self.marks[did].keys():
            self.list.addItem(mark)
        self.list.activate()
