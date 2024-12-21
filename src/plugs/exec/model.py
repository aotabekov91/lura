from plug_qt import vimo

from PyQt6 import QtGui, QtCore, QtWidgets

class ListView(QtWidgets.QListView):
    pass

class Model(QtGui.QStandardItemModel, vimo.Model):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.m_command=['']
        self.m_source=QtGui.QStandardItemModel()

    def applyFilter(self, pattern):
        self.splitPrefix(pattern)
        self.clear()
        for matched in self.getMatched():
            item=QtGui.QStandardItem(matched.text())
            print(matched.text())
            self.appendRow(item)
        # self.dataChanged.emit()
        print(self.rowCount())

    def splitPrefix(self, text):
        if text:
            self.m_command=text.split(' ')
        else:
            self.m_command=['']

    def command(self):
        return self.m_command

    def getMatched(self):
        functions=self.checkFunctions()
        if functions and len(self.m_command)>1: 
            return self.getOptions(functions[0])
        return functions

    def checkFunctions(self):
        functions=[]
        func=self.m_command[0]
        count=self.m_source.rowCount()
        for row in range(count):
            idx=self.m_source.index(row, 0)
            item=self.m_source.itemFromIndex(idx)
            if item:
                item_func=item.text()
                if func==item_func[:len(func)]:
                    functions+=[item]
        return functions

    def getOptions(self, func_item):
        options=[]
        option_val=self.m_command[-1]
        option_pos=len(self.m_command)-2
        option_item=func_item.child(option_pos, 0)
        if option_item:
            for row in range(option_item.rowCount()):
                child=option_item.child(row, 0)
                child_text=child.text()
                child_val=child_text[:len(option_val)]
                if option_val==child_val:
                    options+=[child]
        return options

    def filterAcceptsRow(self, sourceRow, sourceParent):
        parent_row=sourceParent.row()
        idx=self.index(sourceRow, 0, sourceParent)
        item=self.itemFromIndex(idx)
        text=item.text()
        cmd=self.m_command[0]
        if parent_row==-1 and item:
            if cmd==text[:len(cmd)]:
                return True
        elif item:
            arg_level=idx.parent().parent().row()==-1
            if arg_level:
                arg_pos=len(self.m_command)-2
                if idx.row()==arg_pos:
                    return True
            else:
                arg_value=self.m_command[-1]
                if arg_value==text[:len(arg_value)]:
                    return True
        return False

    def populateModel(self, data):
        self.m_source.clear()
        for func, options in data.items():
            func_item=QtGui.QStandardItem(func)
            for name, values in options.items():
                option_item=QtGui.QStandardItem(name)
                for value in values:
                    value_item=QtGui.QStandardItem(value)
                    option_item.appendRow(value_item)
                func_item.appendRow(option_item)
            self.m_source.appendRow(func_item)
