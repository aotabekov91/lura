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

        self.pageInfo = QWidget()
        self.pageInfo.m_layout = QHBoxLayout(self.pageInfo)
        self.pageInfo.m_layout.setContentsMargins(0, 0, 0, 0)
        self.pageInfo.m_layout.setSpacing(0)

        self.title = QLabel()
        self.pageNumber = QLabel()
        self.pageInfo.m_layout.addWidget(self.title)
        self.pageInfo.m_layout.addWidget(self.pageNumber)

        self.commandEdit = QWidget()
        self.commandEdit.m_layout = QFormLayout(self.commandEdit)
        self.commandEdit.m_layout.setContentsMargins(0, 0, 0, 0)
        self.commandEdit.m_layout.setSpacing(0)
        self.commandEdit.hide()

        self.m_edit = MQLineEdit(self)
        self.m_edit.setFixedHeight(20)
        self.m_edit.setStyleSheet('border: 0px')

        self.commandEdit.m_layout.addRow(':', self.m_edit)

        self.window.statusBar().addWidget(self.commandEdit, 1)
        self.window.statusBar().addPermanentWidget(self.pageInfo)

    def setupCommand(self):

        self.m_client = None
        self.m_commands = {}

        self.commandList = QListWidget()

        self.window.setTabLocation(self.commandList, self.location, self.name)

    def hide(self):

        self.m_edit.textChanged.disconnect()
        self.m_edit.clear()
        self.window.deactivateTabWidget(self.commandList)
        self.commandEdit.hide()
        self.window.statusBar().hide()
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
        self.pageInfo.hide()

        self.commandEdit.show()
        self.m_edit.setFocus()

    def addCommands(self, commandList, client):
        for (key, command) in commandList:
            self.m_commands[f'{key} -  {command}'] = getattr(client, command)

    def on_currentPageChanged(self, document, pageNumber):

        numberOfPages = document.numberOfPages()
        self.title.setText(document.filePath())
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