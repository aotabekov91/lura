import sys

import markdown
import mimetypes
import os.path

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKit import *

class Display(QWidget):

    def __init__(self, parent, settings):
        super().__init__(parent.window)
        self.m_parent=parent
        self.window=parent.window
        self.s_settings=settings
        self.location='bottom'
        self.name='Notes'
        self.setup()

    def setup(self):

        self.m_id=None

        self.m_layout=QVBoxLayout(self)
        self.m_layout.setSpacing(0)
        self.m_layout.setContentsMargins(0, 0, 0, 0)

        widget=QWidget()
        widget.m_layout=QHBoxLayout(widget)
        widget.m_layout.setContentsMargins(0, 0, 0, 0)
        widget.m_layout.setSpacing(0)

        self.title=QLineEdit()
        self.title.textChanged.connect(self.on_titleChanged)

        self.switchButton=QPushButton('Switch')
        self.switchButton.pressed.connect(self.on_switchButtonPressed)

        self.saveButton=QPushButton('Save')
        self.saveButton.pressed.connect(self.on_saveButtonPressed)

        widget.m_layout.addWidget(self.title)
        widget.m_layout.addWidget(self.switchButton)
        widget.m_layout.addWidget(self.saveButton)

        self.m_layout.addWidget(widget)

        self.view=QStackedWidget()
        self.content=NQWidget(self.window.plugin.tables)
        self.web=NQWebView()

        self.contentIndex=self.view.addWidget(self.content)
        self.webIndex=self.view.addWidget(self.web)

        self.view.setCurrentIndex(self.contentIndex)

        self.m_layout.addWidget(self.view)

        self.window.setTabLocation(self, self.location, self.name)

        self.setStyleSheet('background-color: white; color: black')

    def open(self, n_id):

        for i in reversed(range(self.m_layout.count())):
            self.m_layout.itemAt(i).widget().setParent(None)

        self.m_id=n_id
        self.web.setId(n_id)
        self.content.setId(n_id)
        self.window.activateTabWidget(self)

    def toggle(self):

        if self.m_layout.count()==0: return
        if not self.isVisible():
            self.window.activateTabWidget(self)
            self.m_dockWidget.titleBarWidget().setStyleSheet(
                    'background-color: white; color: black')
        else:
            self.window.deactivateTabWidget(self)


    def on_titleChanged(self, text):
        self.window.plugin.tables.update(
                'notes', {'id':self.m_id}, {'title':text})

    def on_switchButtonPressed(self):
        widget=self.view.currentWidget()
        if widget==self.web:
            self.view.setCurrentIndex(self.contentIndex)
        else:
            self.view.setCurrentIndex(self.webIndex)
            self.web.load()

    def on_saveButtonPressed(self):
        self.content.save()


class NQWidget(QTextEdit):

    def __init__(self, data):
        super().__init__()
        self.m_data=data
        self.setup()

    def setId(self, nid):
        self.timer.stop()
        self.m_id=nid
        note=self.m_data.get('notes', {'id':self.m_id})
        self.setPlainText(''.join(open(note['loc']).readlines()))
        self.timer.start()

    def setup(self):

        self.changed=False

        self.textChanged.connect(self.on_textChanged)

        self.timer=QTimer()
        self.timer.setInterval(12000)
        self.timer.timeout.connect(self.save)
        self.timer.start()

    def on_textChanged(self):
        self.changed=True

    def save(self):
        if not self.isVisible(): return
        if not self.changed: return
        text=self.toPlainText()
        loc=self.m_data.get('notes', {'id':self.m_id}, 'loc')
        nFile=open(loc, 'w')
        for f in text:
            nFile.write(f)
        self.changed=False

class NQWebView(QWebView):

    def setId(self, nid):
        self.m_id=nid
        note=self.m_data.get('notes', {'id':self.m_id})
        self.m_filePath=note['loc']
        self.load()

    def load(self):
        mFile=open(self.m_filePath)
        mContent=mFile.read()
        self.setHtml(markdown.markdown(mContent))
