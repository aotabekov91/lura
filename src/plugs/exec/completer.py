from PyQt6 import QtWidgets

class Completer(QtWidgets.QCompleter):

    def setCompleter(self):
        model=QtGui.QStandardItemModel()
        for func in self.m_agents.keys():
            item=QtGui.QStandardItem(func)
            model.appendRow(item)
            if func=='installPicks':
                i=QtGui.QStandardItem('installPicks text 1')
                ii=QtGui.QStandardItem('installPicks text 2')
                item.appendRow(i)
                item.appendRow(ii)
        self.m_completer=QtWidgets.QCompleter()
        self.m_completer.setModel(model)
        self.m_completer.splitPath=self.splitPath

    def splitPath(self, path):
        return path.split(' ')

    def setCompletionPrefix(self, str):
        print(str)
        raise
