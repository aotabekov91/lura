from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .widgets import BaseTreeWidget

class Container(QObject):

    dataChanged=pyqtSignal()

    def __init__(self, title):
        super().__init__()
        self.m_title=title
        self.m_kind='container'
        self.m_id=-999

    def getField(self, fieldName, *args):
        return getattr(self, f'm_{fieldName}')

    def setTitle(self, title):
        self.m_title=title
        self.dataChanged.emit()

    def itemData(self):
        return self

