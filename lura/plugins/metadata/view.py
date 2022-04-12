#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .connect import DatabaseConnector

class Metadata(QStackedWidget):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window=parent
        self.db=DatabaseConnector(parent, settings)
        self.location='right'
        self.s_settings=settings
        self.globalKeys={
                'Ctrl+i': (
                    self.toggle,
                    self.window,
                    Qt.WindowShortcut)
                }
        self.name='metadata'
        self.setup()

    def setup(self):

        self.activated=False
        self.kind=None

        self.shortcuts={v:k for k, v in self.s_settings['shortcuts'].items()}

        self.book=['author', 'title', 'year', 'publisher', 'edition', 'address',
                'kind']
        self.paper=[ 'author', 'title', 'journal', 'year', 'volume', 'number',
                'pages', 'kind']
        self.website=['author', 'title', 'url', 'kind']

        self.window.viewChanged.connect(self.on_viewChanged)

        self.createWidgets()

    def on_viewChanged(self):
        if self.activated:
            self.activated=not self.activated
            self.toggle()

    def createWidgets(self):

        self.bookTab=QWidget(self)
        self.bookTab.layout=QFormLayout()

        self.bookFields={}
        for field in self.book:
            qline=QLineEdit(self.bookTab)
            qline.returnPressed.connect(self.commit)
            self.bookTab.layout.addRow(field.title(), qline)
            self.bookFields[field]=qline
        self.bookTab.setLayout(self.bookTab.layout)
        self.bookTabIndex=self.addWidget(self.bookTab)

        self.paperTab=QWidget(self)
        self.paperTab.layout=QFormLayout()

        self.paperFields={}
        for field in self.paper:
            qline=QLineEdit(self.paperTab)
            qline.returnPressed.connect(self.commit)
            self.paperTab.layout.addRow(field.title(), qline)
            self.paperFields[field]=qline
        self.paperTab.setLayout(self.paperTab.layout)
        self.paperTabIndex=self.addWidget(self.paperTab)

        self.websiteTab=QWidget(self)
        self.websiteTab.layout=QFormLayout()

        self.websiteFields={}
        for field in self.website:
            qline=QLineEdit(self.websiteTab)
            qline.returnPressed.connect(self.commit)
            self.websiteTab.layout.addRow(field.title(), qline)
            self.websiteFields[field]=qline
        self.websiteTab.setLayout(self.websiteTab.layout)
        self.websiteTabIndex=self.addWidget(self.websiteTab)

        self.paperTab.hide()
        self.bookTab.hide()
        self.websiteTab.hide()

        self.window.setTabLocation(self, self.location, self.name) 

    def commit(self):
        if self.kind is not None:
            fields=getattr(self, self.kind+'Fields')
            for field, qline in fields.items():
                if not hasattr(self.db, 'set{}'.format(field.title())): continue
                func=getattr(self.db, 'set{}'.format(field.title()))
                func(self.window.view().document(), qline.text())
        self.setFocus()

    def toggle(self, forceShow=False):

        if not self.activated or forceShow:

            self.populateFields()
            self.setCurrentIndex(self.index)
            self.tab.show()
            self.setFocus()
            self.window.activateTabWidget(self)
            self.activated=True

        else:
           
            self.tab.hide()
            self.window.deactivateTabWidget(self)
            self.activated=False

    def populateFields(self):
        did=self.window.document().id()
        data=self.db.get(did)
        self.setKind(data)
        for field, qline in self.fields.items():
            info=''
            if data is not None:
                info=str(dict(data).get(field, ''))
            qline.setText(info)

    def setKind(self, data):
        if data is not None and data['kind']=='paper':
            self.index=self.paperTabIndex
            self.fields=self.paperFields
            self.kind='paper'
            self.tab=self.paperTab
        elif data is not None and data['kind']=='website':
            self.index=self.websiteTabIndex
            self.fields=self.websiteFields
            self.kind='website'
            self.tab=self.websiteTab
        else:
            self.index=self.bookTabIndex
            self.fields=self.bookFields
            self.kind='book'
            self.tab=self.bookTab

    def keyPressEvent(self, event):
        key=event.text()

        if key in self.shortcuts:
            func=getattr(self, self.shortcuts[key])
            func()
        else:
            self.window.keyPressEvent(event)

    def register(self, document):
        self.db.register(document)

    def get(self, did):
        return self.db.get(did)
