from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .connect import DatabaseConnector

class Tags(QObject):

    def __init__(self, parent, settings):
        super().__init__()
        self.window = parent
        self.s_settings = settings
        self.name = 'tags'
        self.db = DatabaseConnector(self) 

    def get(self, m_id, kind='document'):
        return self.db.get(m_id, kind)

    def set(self, m_id, kind, tagList):
        self.db.set(m_id, kind, tagList)
