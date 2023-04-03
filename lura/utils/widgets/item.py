from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .container import Container

class Item(QStandardItem):

    def __init__(self, kind, m_id, window, title=None):
        super().__init__()
        self.m_pathes=[]
        self.m_kind = kind.lower()
        self.m_id = -99 if m_id in ['None', None, ''] else int(m_id)
        self.m_window = window
        self.m_data = window.plugin.tables
        self.m_changedFromOutside=False
        self.setup(title)

    def setup(self, title):
        if self.m_kind == 'container':
            self.m_plugin = Container(title)
            self.m_id=self.m_plugin.id()
        elif self.m_kind == 'document':
            self.m_table='metadata'
            self.m_idName = 'did'
        else:
            self.m_table=self.m_kind+'s'
            self.m_idName = 'id'

        self.setTitle()

    def get(self, *args, **kwargs):
        if self.m_kind == 'container':
            return self.m_plugin.title()
        else:
            return self.m_data.get(
                self.m_table, {self.m_idName: self.m_id}, *args, **kwargs)

    def setTitle(self):
        if self.m_kind=='bookmark':
            title=self.get('text')
        else:
            title=self.get('title')
        if title in ['', None]: title=f'{self.m_kind}: No title'
        if title!=self.text():
            self.m_changedFromOutside=True
            self.setText(title)

    def update(self):
        if self.m_kind=='container':
            self.m_plugin.setTitle(self.text())
        elif self.m_kind=='bookmark':
            updateDict={'text':self.text()}
            self.m_data.update(
                self.m_table, {self.m_idName:self.m_id}, updateDict)
        else:
            updateDict={'title':self.text()}
            self.m_data.update(
                self.m_table, {self.m_idName:self.m_id}, updateDict)

    def copy(self, parent=None):
        copy=Item(self.kind(), self.id(), self.m_window, self.get('title'))
        if parent is not None: parent.appendRow(copy)
        for index in range(self.rowCount()):
            self.child(index).copy(parent=copy)
        return copy

    def kind(self):
        return self.m_kind

    def id(self):
        return self.m_id

    def __eq__(self, other):
        return self.kind()==other.kind() and self.id()==other.id()

    def __hash__(self):
        return hash((self.m_id, self.m_kind))

    def watchFolder(self):
        return self.m_pathes

    def addWatchFolder(self, path):
        if path in self.m_pathes: return
        self.m_pathes+=[path]
