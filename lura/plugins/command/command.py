from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.render import PdfDocument

class Command(QObject):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent
        self.s_settings = settings
        self.name = 'command'
        self.location = 'bottom'
        self.globalKeys = {
            'Ctrl+s': (
                self.toggle,
                self.window,
                Qt.WindowShortcut),
            ':': (
                self.activate,
                self.window,
                Qt.WindowShortcut)
        }
        self.setupStatus()
        self.setupCommand()

    def setupStatus(self):

        self.window.currentPageChanged.connect(self.on_currentPageChanged)
        self.window.viewChanged.connect(self.on_viewChanged)

        self.pageInfo = QWidget()
        self.pageInfo.m_layout = QHBoxLayout(self.pageInfo)
        self.pageInfo.m_layout.setContentsMargins(0, 0, 0, 0)
        self.pageInfo.m_layout.setSpacing(0)

        self.title = QLabel()
        self.pageNumber = QLabel()
        self.pageInfo.m_layout.addWidget(self.title)
        self.pageInfo.m_layout.addWidget(self.pageNumber)

        self.commandEdit = QWidget()
        self.commandEdit.m_layout = QHBoxLayout(self.commandEdit)
        self.commandEdit.m_layout.setContentsMargins(0, 0, 0, 0)
        self.commandEdit.m_layout.setSpacing(0)
        self.commandEdit.hide()

        self.m_edit = MQLineEdit(self)
        self.m_edit.setFixedHeight(20)
        self.m_edit.setStyleSheet('border: 0px')
        self.m_editLabel=QLabel(':')

        # self.commandEdit.m_layout.addRow(':', self.m_edit)
        self.commandEdit.m_layout.addWidget(self.m_editLabel)
        self.commandEdit.m_layout.addWidget(self.m_edit)

        self.window.statusBar().addWidget(self.commandEdit, 1)
        self.window.statusBar().addPermanentWidget(self.pageInfo)

    def setupCommand(self):

        self.m_client = None
        self.m_commands = {}

        self.commandList = QListWidget()

        self.window.setTabLocation(self.commandList, self.location, self.name)

    def hide(self):

        try:
            self.m_edit.textChanged.disconnect()
            self.window.deactivateTabWidget(self.commandList)
        except:
            pass
        self.m_edit.clear()
        self.commandEdit.hide()
        # self.window.statusBar().hide()
        self.commandList.clear()
        for command in self.m_commands:
            self.commandList.addItem(command)

    def on_textChanged(self, text):
        if self.commandList.count() == 1:
            key = self.commandList.item(0).text()
            func = self.m_commands[key]

            self.hide()
            return func()
        else:
            self.commandList.clear()
            for command in self.m_commands:
                if text in command:
                    self.commandList.addItem(command)

    def activate(self):

        self.commandList.clear()

        for command in self.m_commands:
            self.commandList.addItem(command)
        self.m_edit.textChanged.connect(self.on_textChanged)

        self.window.activateTabWidget(self.commandList)
        self.window.statusBar().show()
        # self.pageInfo.hide()

        self.commandEdit.show()
        self.m_edit.setFocus()

    def activateCustom(self, callFunc, label=None):

        self.customClientFunc=callFunc
        self.window.statusBar().show()
        # self.pageInfo.hide()
        if label is not None: self.m_editLabel.setText(label)

        self.m_edit.clear()
        self.m_edit.returnPressed.connect(self.customClientMode)

        self.commandEdit.show()
        self.m_edit.setFocus()

    def customClientMode(self):
        text=self.m_edit.text()
        self.m_editLabel.setText(':')

        self.m_edit.clear()
        self.commandEdit.hide()
        # self.hide()
        func=getattr(self, 'customClientFunc', None)
        if func is None: return
        self.customClientFunc(text)

    def addCommands(self, commandList, client):
        for (key, command) in commandList:
            self.m_commands[f'{key} -  {command}'] = getattr(client, command)

    def on_viewChanged(self, view):
        document=view.document()
        if type(document)==PdfDocument:
            numberOfPages = document.numberOfPages()
            title=self.window.plugin.tables.get(
                    'metadata', {'did':document.id()}, 'title')
            if title in ['', None]: title=document.filePath()
            self.title.setText(title)
            self.pageNumber.setText(f' [0/{numberOfPages}]')
        else:
            title=self.window.plugin.tables.get(
                    'maps', {'id':document.id()}, 'title')
            self.title.setText(title)
            self.pageNumber.setText('')

    def on_currentPageChanged(self, document, pageNumber):

        numberOfPages = document.numberOfPages()
        self.pageNumber.setText(f' [{pageNumber}/{numberOfPages}]')

    def toggle(self):
        if self.window.statusBar().isVisible():
            self.window.statusBar().hide()
        else:
            self.title.show()
            self.pageInfo.show()
            self.window.statusBar().show()

class MQLineEdit(QLineEdit):

    def __init__(self, client):
        super().__init__()
        self.m_client=client

    def keyPressEvent(self,event):
        if event.key()==Qt.Key_Escape:
            self.m_client.hide()
        else:
            super().keyPressEvent(event)
