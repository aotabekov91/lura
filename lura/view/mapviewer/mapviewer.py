import os
from collections import Counter

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.core import Item
from lura.core import MapTree
from lura.view.base import View

from .docmap import DocMap
from .tagmap import TagMap

class MapView(QWidget, View):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent
        self.setup()

    def setup(self):

        self.chosenFor=None

        self.m_layout = QVBoxLayout(self)
        self.m_layout.setSpacing(0)
        self.m_layout.setContentsMargins(0,0,0,0)
        self.m_title = MQLineEdit()

        self.m_docMap = DocMap(self.window)
        self.m_docMap.open = self.openNode
        self.m_docMap.currentItemChanged.connect(
                self.window.mapItemChanged)

        self.m_tagMap= TagMap(self.window)
        self.m_tagMap.open = self.openNode
        self.m_tagMap.currentItemChanged.connect(
                self.window.mapItemChanged)

        self.stack=QStackedWidget()

        self.m_docIndex=self.stack.addWidget(self.m_docMap)
        self.m_tagIndex=self.stack.addWidget(self.m_tagMap)

        commandList=[
                ('mot', 'openTagView'),
                # ('maf', 'addFolder'),
                # ('mad', 'addDocument'),
                # ('mdd', 'deleteDocument'),
                # ('maw', 'addWatchFolder'),
                # ('muw', 'updateWatchFolder'),
                # ('msa', 'activateSorting'),
                # ('msd', 'deactivateSorting'),
                # ('mfa', 'activateFiltering'),
                # ('mfd', 'deactivateFiltering'),
                # ('mtt', 'showTagTree'),
                # ('mmd', 'moveDocumentTo'),
                ]

        self.window.plugin.command.addCommands(commandList, self)

        self.m_layout.addWidget(self.m_title)
        self.m_layout.addWidget(self.stack)

    def tree(self):
        return self.m_docMap

    def document(self):
        return self.m_docMap.model()

    def setFocus(self):
        self.stack.currentWidget().setFocus()

    def open(self, document):

        self.m_document = document
        self.m_docMap.setModel(self.m_document.model())
        self.m_docMap.model().itemChanged.connect(self.on_itemChanged)

        self.stack.setCurrentIndex(self.m_docIndex)

        self.show()
        self.m_docMap.show()
        self.m_docMap.setFocus()

        self.m_title.show()
        self.m_title.setMap(document.id(), self.window)

    def openTagView(self):
        if self.m_docMap.model() is None: return
        self.stack.setCurrentIndex(self.m_tagIndex)
        self.m_tagMap.openModel(self.m_docMap.model())

        self.m_title.hide()
        self.m_tagMap.show()
        self.m_tagMap.setFocus()

    def openNode(self, item=None):

        if item is None: item = self.stack.currentWidget().currentItem()
        if item is None: return

        if item.kind() == 'annotation':

            b = item.get('position').split(':')
            topLeft = QPointF(float(b[0]), float(b[1]))
            did = item.get('did')
            pageNumber = item.get('page')
            filePath = self.window.plugin.tables.get(
                'documents', {'id': did}, 'loc')

            self.window.open(filePath)
            self.window.view().jumpToPage(
                pageNumber, topLeft.x(), 0.95*topLeft.y())

        elif item.kind() == 'document':

            filePath = self.window.plugin.tables.get(
                'documents', {'id': item.id()}, 'loc')
            self.window.open(filePath)


    def on_itemChanged(self, item):
        item.update()
        if item.kind() == 'container':
            self.m_document.update()
        if item.m_changedFromOutside:
            item.m_changedFromOutside=False
            return
        self.window.titleChanged.emit(self)

    def event(self, event):
        if event.type()==QEvent.Enter: self.window.setView(self)
        return super().event(event)

class MQLineEdit(QLineEdit):

    def __init__(self):
        super().__init__()
        self.textChanged.connect(self.on_textChanged)

    def setMap(self, m_id, window):
        self.window=window
        self.m_id=m_id
        self.setText(self.window.plugin.tables.get(
            'maps', {'id':self.m_id}, 'title'))

    def on_textChanged(self, text):
        self.window.plugin.tables.update(
                'maps', {'id':self.m_id}, {'title':text})
