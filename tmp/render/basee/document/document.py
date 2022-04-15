from PyQt5.QtCore import *

class Document(QObject):

    annotationAdded=pyqtSignal(object)
    annotationRegistered=pyqtSignal(object)

    def __init__(self, filePath=None):
        super().__init__()
        self.m_data=None
        self.m_id=None
        self.m_filePath=filePath


    def __eq__(self, other):
        return self.m_data==other.m_data

    def __hash__(self):
        return hash(self.m_data)
    
    def setId(self, did):
        self.m_id=did
        if did is not None: self.setRegistered(True)

    def data(self):
        return self.m_data
