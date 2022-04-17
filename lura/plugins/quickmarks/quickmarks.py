from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.render.pdf import PdfDocument


class Quickmarks(QListWidget):

    def __init__(self, parent, settings):
        super().__init__()
        self.window = parent
        self.s_settings = settings
        self.name = 'quickmarks'
        self.location = 'bottom'
        self.globalKeys = {
            'Ctrl+m': (
                self.set,
                self.window,
                Qt.WidgetWithChildrenShortcut,
            ),
            'Ctrl+g': (
                self.goto,
                self.window,
                Qt.WidgetWithChildrenShortcut,
            ),
        }
        self.setup()

    def setup(self):

        self.marks = {}
        self.window.setTabLocation(self, self.location, self.name)

    def toggle(self):
        if not self.activated:
            self.window.activateStatusBar(self)
            self.activated = True
        else:
            self.window.deactivateStatusBar(self)
            self.activated = False

    def set(self):
        view = self.window.view()
        if view is None or type(view.document()) != PdfDocument:
            return
        self.window.plugin.command.activateCustom(
            self._set, 'Mark: ')

    def _set(self, mark):
        if mark=='': return
        did = self.window.view().document().id()
        page = self.window.view().currentPage()
        left, top = self.window.view().saveLeftAndTop()

        if not did in self.marks:
            self.marks[did] = {}

        self.marks[did][mark] = (page, left, top)

    def goto(self):
        view = self.window.view()
        if view is None or type(view.document()) != PdfDocument:
            return
        did = view.document().id()
        if not did in self.marks:
            return
        self.showList(did)
        self.window.plugin.command.activateCustom(self._goto, 'Jump: ')

    def _goto(self, mark):
        if mark=='': return
        self.window.deactivateTabWidget(self)
        did = self.window.view().document().id()
        if not mark in self.marks[did]:
            return
        page, left, top = self.marks[did][mark]
        print(self.marks, mark, page)
        self.window.view().jumpToPage(page, left, top)

    def showList(self, did):
        self.clear()
        for mark in self.marks[did].keys():
            self.addItem(mark)
        self.window.activateTabWidget(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.window.deactivateTabWidget(self)
            self.window.view().setFocus()
