from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ...actions import Actions
from lura.utils import classify

class StatusBar(QStatusBar):

    keyPressEventOccurred=pyqtSignal(object)

    def __init__(self, app):
        super(StatusBar, self).__init__()
        self.app=app
        self.client=None

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
        layout.setContentsMargins(0,0,0,0)
        self.setLayout(layout)

        self.command_info=QLabel('command')
        self.command_edit=QLineEdit(parent=self)
        self.detail_info=QLabel('detail')
        self.document_info=QLabel('document_hash')
        self.page_info=QLabel('test')

        self.addWidget(self.command_info)
        self.addWidget(self.command_edit, 1)
        self.addWidget(self.detail_info)
        self.addPermanentWidget(self.document_info)
        self.addPermanentWidget(self.page_info, 0)
        self.setFixedHeight(20)

        self.command_info.hide()
        self.command_edit.hide()
        self.detail_info.hide()

        self.setStyleSheet(self.style_sheet)
        self.setSizeGripEnabled(False)

        self.hide()

    def connect(self):
        self.app.window.display.currentPageChanged.connect(self.on_currentPageChanged)
        self.app.window.display.viewChanged.connect(self.on_viewChanged)

    def setActions(self):
        self.connect()
        self.actions=Actions(self.app, 'Statusbar', self)

    def on_viewChanged(self, view):
        doc_hash=view.document().hash()
        self.setDocumentInfo(doc_hash)

    def on_currentPageChanged(self, document, page_number):
        total_pages=document.numberOfPages()
        self.setPageInfo(f'{page_number}/{total_pages}')

    def commandEdit(self):
        return self.command_edit

    def setCommandInfo(self, text):
        self.command_info.setText(text)
        self.command_info.show()

    def setDetailInfo(self, text):
        self.detail_info.setText(text)
        self.detail_info.show()

    def setDocumentInfo(self, text):
        self.document_info.setText(text)

    def setPageInfo(self, text):
        self.page_info.setText(text)

    def setClient(self, client=None):
        if self.client:
            self.client.deactivate()
        self.client=client
        if not self.client:
            self.app.window.display.focusCurrentView()

    def focusCommandEdit(self):
        self.command_edit.show()
        self.command_edit.setFocus()
        self.show()

    def clearCommand(self):
        self.command_info.clear()
        self.command_edit.clear()
        self.command_info.hide()
        self.command_edit.hide()

    @classify(parent='window', context=Qt.WindowShortcut)
    def toggle(self, focus=False):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            if focus: self.setFocus()

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.hide()
        elif event.key()==Qt.Key_I and self.command_edit.isVisible():
            self.command_edit.setFocus()
        self.keyPressEventOccurred.emit(event)
