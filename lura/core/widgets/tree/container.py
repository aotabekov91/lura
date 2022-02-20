from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .widgets import BaseTreeWidget

class Container(QObject):

    dataChanged=pyqtSignal()

    def __init__(self, title):
        super().__init__()
        self.m_title=title

    def title(self):
        return self.m_title

    def setTitle(self, title):
        self.m_title=title
        self.dataChanged.emit()

    def widget(self):
        return BaseTreeWidget(self)

    def id(self):
        return -999

    def kind(self):
        return 'container'

    def itemData(self):
        return self

    def tags(self):
        return ''

    def setTags(self):
        pass
