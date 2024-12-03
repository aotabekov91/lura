from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Container(QObject):

    count=-1
    dataChanged=pyqtSignal()

    def __init__(self, title):
        super().__init__()
        self.m_title=title
        self.m_kind='container'
        Container.count+=1
        self.m_id=Container.count

    def kind(self):
        return self.m_kind

    def id(self):
        return self.m_id

    def title(self):
        return self.m_title

    def setTitle(self, title):
        self.m_title=title
