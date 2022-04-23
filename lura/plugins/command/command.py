from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.core.miscel import Item
from lura.render import PdfDocument

class Command(QObject):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent
        self.s_settings = settings
        self.name = 'command'
        self.location = 'bottom'
        self.globalKeys = {
            ':': (
                self.activate,
                self.window,
                Qt.WindowShortcut)
        }

        self.setup()

    def setup(self):

        self.m_client = None
        self.m_commands = {}

        self.commandList = QListWidget()

        self.commandEdit = QWidget()
        self.commandEdit.m_layout = QHBoxLayout(self.commandEdit)
        self.commandEdit.m_layout.setContentsMargins(0, 0, 0, 0)
        self.commandEdit.m_layout.setSpacing(0)
        self.commandEdit.hide()

        self.m_edit = MQLineEdit(self)
        self.m_edit.setFixedHeight(20)
        self.m_edit.setStyleSheet('border: 0px')
        self.m_editLabel=QLabel(':')

        self.commandEdit.m_layout.addWidget(self.m_editLabel)
        self.commandEdit.m_layout.addWidget(self.m_edit)

        self.window.statusBar().addWidget(self.commandEdit, 1)
        self.window.setTabLocation(self.commandList, self.location, self.name)

    def hide(self):

        try:
            self.m_edit.textChanged.disconnect()
            self.window.deactivateTabWidget(self.commandList)
        except:
            pass
        self.m_edit.clear()
        self.commandEdit.hide()
        self.commandList.hide()
        self.commandList.clear()
        for command in self.m_commands:
            self.commandList.addItem(command)

        self.window.setFocus()

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

        self.window.setCorner(Qt.BottomLeftCorner, Qt.BottomDockWidgetArea)
        self.window.plugin.pageinfo.hide()
        self.commandEdit.show()
        self.m_edit.setFocus()

    def activateCustom(self, callFunc, label=None, contCallFunc=None, text=None):

        self.window.plugin.pageinfo.hide()
        self.wasStatusBarVisible=self.window.statusBar().isVisible()

        self.customClientFunc=callFunc
        self.contCallFunc=contCallFunc

        self.window.statusBar().show()
        if label is not None: self.m_editLabel.setText(label)

        self.m_edit.clear()
        self.m_edit.returnPressed.connect(self.customClientMode)
        if contCallFunc is not None:
            self.m_edit.textChanged.connect(self.contCallFunc)
        if text is not None:
            self.m_edit.setText(text)

        self.commandEdit.show()
        self.m_edit.setFocus()

    def customClientMode(self):

        self.window.plugin.pageinfo.show()
        if not self.wasStatusBarVisible: self.window.statusBar().hide()

        text=self.m_edit.text()
        self.m_editLabel.setText(':')

        self.m_edit.clear()
        self.commandEdit.hide()
        self.window.setCorner(Qt.BottomLeftCorner, Qt.LeftDockWidgetArea)

        func=getattr(self, 'customClientFunc', None)
        if func is None: return

        try:
            self.m_edit.returnPressed.disconnect()
            self.m_edit.textChanged.disconnect()
        except:
            pass

        self.customClientFunc(text)

    def addCommands(self, commandList, client):
        for (key, command) in commandList:
            self.m_commands[f'{key} -  {command}'] = getattr(client, command)


class MQLineEdit(QLineEdit):

    def __init__(self, client):
        super().__init__()
        self.m_client=client

    def keyPressEvent(self,event):

        wasVisible=getattr(self.m_client, 'wasStatusBarVisible', None)

        if event.key()==Qt.Key_Escape:
            self.m_client.hide()
            if not wasVisible:
                self.m_client.window.statusBar().hide()
        else:
            super().keyPressEvent(event)
