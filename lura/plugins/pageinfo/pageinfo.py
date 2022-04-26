from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.core.miscel import Item
from lura.render import PdfDocument

class PageInfo(QWidget):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent
        self.s_settings = settings
        self.name = 'pageinfo'

        self.globalKeys = {
            'Ctrl+s': (
                self.toggle,
                self.window,
                Qt.WindowShortcut),
        }

        self.setup()

    def setup(self):

        self.window.viewChanged.connect(self.on_viewChanged)
        self.window.mapItemChanged.connect(self.on_viewChanged)
        self.window.documentTagged.connect(self.on_documentTagged)
        self.window.currentPageChanged.connect(self.on_currentPageChanged)

        self.m_layout = QHBoxLayout(self)
        self.m_layout.setSpacing(0)
        self.m_layout.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel()
        self.mode=QLabel()
        self.pageNumber = QLabel()
        self.tags=QLabel()

        self.m_layout.addWidget(self.title)
        self.m_layout.addWidget(self.mode)
        self.m_layout.addWidget(self.tags)
        self.m_layout.addWidget(self.pageNumber)

        self.window.statusBar().addPermanentWidget(self)

    def on_documentTagged(self, m_id, kind, tagList, sender):
        text='; '.join(tagList)
        self.tags.setText(f' [{text}] ')

    def on_viewChanged(self, view):

        if view is None: return

        if type(view)==Item:

            title=view.get('title')

            parent=view.parent()
            if parent is None:
                parent=view.index().model().invisibleRootItem()

            data=self.window.plugin.tags.get(
                    view.id(), view.kind())
            tags=''
            if data is not None: 
                tags='; '.join(data)

            mode=f'{view.kind().title()} {view.id()}'

            pageNumber=view.row()+1
            numberOfPages=parent.rowCount()

        elif type(view.document())==PdfDocument:
            document=view.document()
            title=self.window.plugin.tables.get(
                    'metadata', {'did':document.id()}, 'title')
            if title in ['', None]: title=document.filePath()
            data=self.window.plugin.tags.get(
                    document.id(), 'document')
            tags=''
            if data is not None:
                tags='; '.join(data)

            numberOfPages = document.numberOfPages()
            pageNumber=view.currentPage()
            mode=f'Document {document.id()}'

        else:
        
            title=mode=tags=pageNumber=''

        self.title.setText(title)
        self.mode.setText(f' [{mode}] ')
        self.tags.setText(f' [{tags}] ')
        if pageNumber!='':
            pageNumber=f'{pageNumber}/{numberOfPages}'
        self.pageNumber.setText(f' [{pageNumber}]')

    def on_currentPageChanged(self, document, pageNumber):
        numberOfPages = document.numberOfPages()
        self.pageNumber.setText(f' [{pageNumber}/{numberOfPages}]')

    def toggle(self):
        if self.window.statusBar().isVisible():
            self.window.statusBar().hide()
        else:
            self.show()
            self.window.statusBar().show()
