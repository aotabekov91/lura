from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Container(QObject):

    dataChanged=pyqtSignal()

    def __init__(self, title):
        super().__init__()
        self.m_title=title
        self.m_kind='container'
        self.m_id=-999

    def kind(self):
        return self.m_kind

    def id(self):
        return self.m_id

    def title(self):
        return self.m_title

    def setTitle(self, title):
        self.m_title=title
