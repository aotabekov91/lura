from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from speechToCommand.utils.helper import command
from .components import InputWidget
from .components import CustomListWidget, CustomListItem

class ListWidget (QWidget):

    returnPressed=pyqtSignal()
    deleteWanted=pyqtSignal()
    contentUpdateOccurred=pyqtSignal(int, str)
    keyPressEventOccurred=pyqtSignal(object)

    def __init__(self, app, parent, location=None, name=None):
        super(ListWidget, self).__init__(app.window)

        self.style_sheet='''
            QWidget{
                font-size: 14px;
                color: white;
                border-width: 0px;
                background-color: #101010; 
                border-color: transparent;
                }
            QWidget#mainWidget{
                border-radius: 10px;
                border-style: outset;
                background-color: transparent; 
                }
                '''
        
        self.app=app
        self.name=name
        self.m_parent=parent
        self.location=location

        self.dlist = []

        self.input=InputWidget(self)
        self.list=CustomListWidget(self)

        self.setStyleSheet(self.style_sheet)
        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.input)
        layout.addWidget(self.list)

        self.setLayout(layout)

        self.input.textChanged.connect(self.onInputTextChanged)
        self.input.returnPressed.connect(self.returnPressed)

        self.app.window.setTabLocation(self, self.location, self.name)

    def setText(self, text):
        self.input.setText(text)

    def deactivate(self):
        self.app.window.deactivateTabWidget(self)

    def activate(self):
        self.app.window.activateTabWidget(self)
        self.input.setFocus()

    def setList(self, dlist):
        self.dlist=dlist
        self.addItems(dlist)
        self.show()

    def applyFilter(self, text, itemData):
        if hasattr(self.m_parent, 'applyFilter'):
            return self.m_parent.applyFilter(text, itemData)
        else:
            fields= f"{itemData['title']}  {itemData['content']}"
            return text in fields

    def onInputTextChanged(self):
        if len(self.dlist)==0: return
        text=self.input.text()
        self.list.clear()
        dlist = []
        for i, w in enumerate(self.dlist):
            if self.applyFilter(text.lower(),w ): dlist += [w]
        self.addItems(dlist, False)

    def sizeHint(self):
        hint=self.input.sizeHint()
        if self.list.count()>0:
            list_hint=self.list.sizeHint()
            hint=QSize(hint.width(), hint.height()+list_hint.height())
        return hint

    def addItems(self, dlist, save=True):
        self.list.clear()
        if save: self.dlist = dlist
        if len(dlist)==0: dlist=[{'title': 'No matches are found'}]
        widgets=[]
        for d in dlist:
            widgets+=[self.addItem(d)]
        width=self.size().width()
        height=0
        for i, w in enumerate(widgets):
            if w.sizeHint().height()>height:
                height=w.sizeHint().height()
        hint=QSize(width, height)
        for i in range(len(widgets)):
            item=self.list.item(i)
            item.setSizeHint(hint)
        self.list.setCurrentRow(0)

    def addItem(self, w):
        item = QListWidgetItem(self.list)
        item.itemData = w

        widget = CustomListItem(w)
        widget.contentUpdateOccurred.connect(self.contentUpdateOccurred)

        self.list.addItem(item)
        self.list.setItemWidget(item, widget)
        return widget

    def moveAction(self, request={}, crement=-1):
        crow = self.list.currentRow()
        if crow==None: return
        crow += crement
        if crow < 0:
            crow = self.list.count()-1
        elif crow >= self.list.count():
            crow = 0
        self.setCurrentRow(crow)

    def setCurrentRow(self, index):
        if index<0:
            index=0
        elif index-1>self.list.count():
            index=self.index.count()-1
        self.list.setCurrentRow(index)

    def currentRow(self):
        return self.list.currentRow()

    def setCurrentItem(self, iid):
        for i in range(self.list.count()):
            item=self.list.item(i)
            if item.itemData['id']==iid:
                self.list.setCurrentItem(item)
                return

    def currentItem(self):
        return self.list.currentItem()

    def keyPressEvent(self, event):
        self.keyPressEventOccurred.emit(event)
        if event.key() in [Qt.Key_Down, Qt.Key_Up]:
            self.list.keyPressEvent(event)
        elif event.key() in [Qt.Key_Q, Qt.Key_Escape]:
            self.m_parent.deactivate()
        elif event.key()==Qt.Key_I:
            self.input.setFocus()
        elif event.modifiers() or self.list.hasFocus():
            if event.key() in [Qt.Key_J, Qt.Key_N]:
                self.moveAction(crement=1)
            elif event.key() in [Qt.Key_K, Qt.Key_P]:
                self.moveAction(crement=-1)
            elif event.key() in  [Qt.Key_L, Qt.Key_M, Qt.Key_Enter]:
                self.returnPressed.emit()
            elif event.key()==Qt.Key_W:
                self.deleteWanted.emit()
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

    def clearInput(self):
        self.input.clear()

    def clear(self):
        self.dlist=[]
        self.clearInput()
        self.list.clear()
