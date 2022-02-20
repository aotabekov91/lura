from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class QuickmarkModel(QAbstractTableModel):

    def __init__(self, parent):
        super().__init__()
        self.m_parent=parent

    def rowCount(self, index):
        return len(self.m_parent.markActions)

    def columnCount(self, index):
        return 2

    def data(self, index, role):
        if role == Qt.TextAlignmentRole: 
            align=Qt.AlignVCenter
            if index.column()==0:
                align=align|Qt.AlignHCenter
            return align
        if role != Qt.DisplayRole and role != Qt.EditRole: return 

        data=list(self.m_parent.markActions.values())[index.row()]
        if index.column()==0: return data['key']
        elif index.column()==1: return data['comment']

    def flags(self, index):
        flags=super().flags(index)
        if index.column()==1:
            return flags|Qt.ItemIsEditable
        return flags

    def setData(self, index, value, role):
        if role==Qt.EditRole:
            for i, key, data in enumerate(self.m_parent.markActions.items()):
                if i==index.row():
                    if index.column()==0:
                        updatedData={'key':value}
                        data['key']=value
                    elif index.column()==1:
                        updatedData={'comment':value}
                        data['comment']=value
                    self.m_parent.db.updateRow({'field':'id','value':data['id']}, updatedData)
                    self.dataChanged.emit(index, index)
                    return True

    def headerData(self, section, orientation, role):
        if orientation!=Qt.Horizontal or role!=Qt.DisplayRole: return 
        elif section==0: return 'Key'
        elif section==1: return 'Comment'

