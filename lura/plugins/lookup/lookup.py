from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from notes import _get_definition 
from lura.core.widgets import CustomTree

class Lookup(CustomTree):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window=parent
        self.s_settings=settings
        self.name = 'wordLookup'
        self.globalKeys={
                'Ctrl+l': (
                    self.toggle,
                    self.window,
                    Qt.WindowShortcut)
                }
        self.setup()

    def setup(self):

        self.activated=False
        self.cursor=self.window.plugin.view.cursor
        self.setModel(QStandardItemModel())
        self.header().setVisible(False)
        self.window.setTabLocation(self, 'bottom', 'Definition')

    def on_mouseDoubleClicked(self, event, pageItem, view):

        if not self.activated: return

        print('a')
        chosen=self.cursor.selectWordUnderCursor(event, pageItem)

        if chosen is None: return

        word, self.area=chosen

        pageItem.pageHasBeenJustPainted.connect(self.drawSelectedWordRectangle)
        pageItem.refresh(dropCachedPixmap=True)

        for w in [',', '.', ':', '?', '!']:
            word=word.replace(w, '')

        definitions=_get_definition('en', word, False)
        self.prepareTreeView(word, definitions)
        self.window.activateTabWidget(self)
        self.setFocus()

    def prepareTreeView(self, word, definitions):

        self.model().clear()
        rootNode=self.model().invisibleRootItem()

        kind={}
        for d in definitions:
            key='{} {} {}'.format(word, 
                d['fields']['PartOfSpeech'],
                d['fields']['IPA']
                )
            kind[key]=QStandardItem(key)


        for d in definitions:
            key='{} {} {}'.format(word, 
                d['fields']['PartOfSpeech'],
                d['fields']['IPA']
                )

            item=kind[key]
            exp=QStandardItem(d['fields']['Definition'])
            example=QStandardItem(d['fields']['Example'])
            exp.appendRow(example)
            item.appendRow(exp)

        for item in kind.values():
            rootNode.appendRow(item)
        
    def drawSelectedWordRectangle(self, painter, options, widget):
        if self.activated:
            painter.setPen(QPen(Qt.red, 0.0))
            painter.drawRect(self.area)

    def toggle(self):

        if not self.activated: 

            self.activated=True
            self.window.mouseDoubleClickOccured.connect(self.on_mouseDoubleClicked)

        else:

            self.activated=False
            self.window.deactivateTabWidget(self)
            self.window.mouseDoubleClickOccured.disconnect(self.on_mouseDoubleClicked)

    def selectArea(self, painter, options, widgets, pageItem):
        painter.fillRect(self.rect, QColor(0, 255, 0, 127))
        pageItem.pageHasBeenJustPainted.disconnect(self.selectArea)

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.toggle()
        else:
            super().keyPressEvent(event)
