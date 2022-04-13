from datetime import datetime

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .proxy import BaseProxyWidget

class Item(QStandardItem):

    def __init__(self, data):
        super().__init__(data.getField('title'))
        self.m_data=data
        self.connect()
        self.setCreateTime(datetime.now().timestamp())
        self.setup()

    def setup(self):
        self.m_proxy=None

    def setCreateTime(self, time):
        self.m_createTime=time

    def createTime(self):
        return self.m_createTime

    def connect(self):
        if hasattr(self.m_data, 'dataChanged'):
            self.m_data.dataChanged.connect(self.emitDataChanged)

    def setWidget(self, widget):
        widget.sizeChanged.connect(self.emitDataChanged)
        self.m_proxy=BaseProxyWidget(widget, self)

    def proxy(self):
        if self.m_proxy is None: 
            self.setWidget(self.m_data.widget())
        return self.m_proxy

    def itemData(self):
        return self.m_data

    def copy(self, parent=None, shallow=False):
        copy=Item(self.itemData())
        if shallow: return copy
        if parent is not None: parent.appendRow(copy)
        for index in range(self.rowCount()):
            self.child(index).copy(copy)
        return copy

    def isEqual(self, other):
        if self.itemData().kind()==other.itemData().kind():
            if self.itemData().id()==other.itemData().id():
                return True
        return False

    def hide(self):
        if self.m_proxy is None: self.setWidget(self.m_data.widget())
        self.m_proxy.hide()

    def show(self):
        if self.m_proxy is None: self.setWidget
        self.m_proxy.show()

    def update(self):
        self.m_proxy.update()

    def isVisible(self):
        return self.proxy().isVisible()
