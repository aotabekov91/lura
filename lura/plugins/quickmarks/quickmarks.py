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
        print(type(view))
        if view is None: return
        self.window.plugin.command.activateCustom(self._set, 'Mark: ')

    def _set(self, mark):
        if mark=='': return
        view = self.window.view()
        if type(view.document()) == PdfDocument:
            did = self.window.view().document().id()
            page = self.window.view().currentPage()
            left, top = self.window.view().saveLeftAndTop()
        else:
            tree=self.window.view().tree()
            did=tree.model()
            page=tree.currentItem()
            left, top=None, None

        if not did in self.marks: self.marks[did] = {}

        self.marks[did][mark] = (page, left, top)
        print(self.marks)

    def goto(self):
        view = self.window.view()
        if view is None: return
        if type(view.document()) == PdfDocument:
            did = view.document().id()
        else:
            did=view.tree().model()

        if not did in self.marks: return
        self.showList(did)
        self.window.plugin.command.activateCustom(self._goto, 'Jump: ')

    def _goto(self, mark):
        if mark=='': return
        self.window.deactivateTabWidget(self)

        view = self.window.view()
        if type(view.document()) == PdfDocument:
            did = self.window.view().document().id()
        else:
            did=self.window.view().tree().model()

        if not mark in self.marks[did]: return

        page, left, top = self.marks[did][mark]

        if type(view.document()) == PdfDocument:
            self.window.view().jumpToPage(page, left, top)
            self.window.view().setFocus()
        else:
            self.window.view().tree().setCurrentIndex(page.index())
            self.window.view().tree().setFocus()

    def showList(self, did):
        self.clear()
        for mark in self.marks[did].keys():
            self.addItem(mark)
        self.window.activateTabWidget(self)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.window.deactivateTabWidget(self)
            self.window.view().setFocus()
