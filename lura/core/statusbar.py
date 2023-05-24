from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Configure, register

class StatusBar(QStatusBar):

    hideWanted=pyqtSignal()
    keyPressEventOccurred=pyqtSignal(object)

    def __init__(self, window):

        super(StatusBar, self).__init__()

        self.clients={}

        self.window=window
        self.configure=Configure(window.app, 'Statusbar', self)

        self.window.display.viewChanged.connect(self.on_viewChanged)
        self.window.display.currentPageChanged.connect(self.on_currentPageChanged)

        self.setUI()
        self.hide()

    def setUI(self):

        self.style_sheet='''
            QLineEdit {
                background-color: transparent;
                border-color: transparent;
                border-width: 0px;
                border-radius: 0px;
                }
            QLabel{
                background-color: transparent;
                }
                '''

        layout=self.layout()
        layout.setContentsMargins(1,1,1,1)
        self.setLayout(layout)

        self.info=QLabel('Info')
        self.page=QLabel('Page')
        self.edit=QLineEdit(self)
        self.detail=QLabel('Detail')
        self.document=QLabel('Document')

        self.setFixedHeight(25)

        self.addWidget(self.info)
        self.addWidget(self.edit, 1)
        self.addWidget(self.detail)

        self.addPermanentWidget(self.document)
        self.addPermanentWidget(self.page, 0)

        self.info.hide()
        self.edit.hide()
        self.detail.hide()

        self.setSizeGripEnabled(False)
        self.setStyleSheet(self.style_sheet)

    def installEventFilter(self, listener):

        super().installEventFilter(listener)
        self.info.installEventFilter(listener)
        self.page.installEventFilter(listener)
        self.detail.installEventFilter(listener)
        self.document.installEventFilter(listener)

    def removeEventFilter(self, listener):

        super().removeEventFilter(listener)
        self.info.removeEventFilter(listener)
        self.edit.removeEventFilter(listener)
        self.page.removeEventFilter(listener)
        self.detail.removeEventFilter(listener)
        self.document.removeEventFilter(listener)

    def on_viewChanged(self, view):

        doc_hash=view.document().hash()
        self.document.setText(doc_hash)
        self.on_currentPageChanged(view.document())

    def on_currentPageChanged(self, document, current_page=None, prev_page=None):

        if not current_page: current_page=self.window.display.view.currentPage()
        total_pages=document.numberOfPages()
        self.page.setText(f'{current_page}/{total_pages}')

    @register('tb', modes=['normal', 'command'])
    def toggle(self):

        if self.isVisible():
            self.hide()
        else:
            self.show()

    def clear(self, fields=['info', 'edit', 'detail']):

        for f in fields:
            field=getattr(self, f)
            field.setText('')
            field.hide()

    def setData(self, data=None):

        self.clear()

        if not data: data=self.clients.get('prev', {})

        self.clients['prev']=self.clients.get('current', {})
        if 'client' in self.clients['prev']:
            self.clients['prev']['visible']=self.isVisible()
        self.clients['current']=data

        for f, v in data.items():
            if f in ['edit', 'info', 'detail', 'page', 'document']:
                field=getattr(self, f, None)
                if field:
                    field.setText(v)
                    field.show()

        if data.get('visible', False): 
            self.show()
        else:
            super().hide()

    def hide(self):

        data=self.clients.get('prev', {})
        self.setData(data)

        if not getattr(data, 'visible', False): super().hide()

    def keyPressEvent(self, event):

        self.keyPressEventOccurred.emit(event)
        if event.key()==Qt.Key_Escape:
            self.hide()
            self.hideWanted.emit()
        elif event.key()==Qt.Key_I and self.edit.isVisible():
            self.edit.setFocus()
        else:
            super().keyPressEvent(event)
