from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Display(QWidget):

    keyPressEventOccurred=pyqtSignal(object)
    deleteButtonPressed=pyqtSignal(int)
    contentUpdateOccurred=pyqtSignal(int, str)

    def __init__(self, app, parent, location=None, name=None, filter_kind='combo'):
        super().__init__(app.window)

        self.m_data=[]
        self.filter_kind=filter_kind

        self.app=app
        self.name=name
        self.m_parent=parent
        self.location=location

        self.m_layout=QVBoxLayout(self)
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: green; color: red")

        self.filter=QLineEdit()
        self.filter.textChanged.connect(self.onInputTextChanged)
        self.list=QListWidget(self)
        self.list.setWordWrap(True)
        self.list.adjustSize()

        self.m_layout.addWidget(self.filter)
        self.m_layout.addWidget(self.list)

        self.app.window.setTabLocation(self, self.location, self.name)

    def clear(self):
        self.filter.clear()

    def add_items(self, dlist, save=True):
        self.list.clear()
        if save: self.dlist = dlist
        if len(dlist)==0: dlist=[{'top': 'No matches are found'}]
        for d in dlist:
            self.add_item(d)
        self.list.setCurrentRow(0)
        self.adjustSize()

    def add_item(self, w):
        item = QListWidgetItem(self.list)
        widget = DisplayItem(w)
        widget.deleteButtonPressed.connect(self.deleteButtonPressed)
        widget.contentUpdateOccurred.connect(self.contentUpdateOccurred)
        print(widget.size())
        widget.adjustSize()

        self.list.addItem(item)
        self.list.setItemWidget(item, widget)
        print(widget.size())

    def setList(self, dlist):
        self.dlist=dlist
        self.add_items(dlist)

    def onInputTextChanged(self):
        if len(self.dlist)==0: return
        text=self.filter.text()
        self.list.clear()
        dlist = []
        for i, w in enumerate(self.dlist):
            text_up = w['top']
            text_down = w.get('down', '')
            if (text.lower() in text_up.lower() or text.lower() in text_down.lower()):
                dlist += [w]
        self.add_items(dlist, False)

    def on_deleteButtonPressed(self, iid):
        self.deleteButtonPressed.emit(iid)
        raise

    def deactivate(self):
        self.app.window.deactivateTabWidget(self)

    def activate(self):
        self.app.window.activateTabWidget(self)
        self.setFocus()

    def moveAction(self, request={}, crement=-1):
        crow = self.list.currentRow()
        if crow==None: return
        crow += crement
        if crow < 0:
            crow = self.list.count()-1
        elif crow >= self.list.count():
            crow = 0
        self.list.setCurrentRow(crow)

    def keyPressEvent(self, event):
        self.keyPressEventOccurred.emit(event)
        if event.key() in [Qt.Key_Down, Qt.Key_Up]:
            self.list.keyPressEvent(event)
        elif event.key()==Qt.Key_I:
            self.filter.setFocus()
        elif event.modifiers() or self.list.hasFocus():
            if event.key() in [Qt.Key_J, Qt.Key_N]:
                self.moveAction(crement=1)
            elif event.key() in [Qt.Key_K, Qt.Key_P]:
                self.moveAction(crement=-1)
            elif event.key() in  [Qt.Key_L, Qt.Key_M, Qt.Key_Enter]:
                self.mode.confirmAction()
            else:
                super().keyPressEvent(event)
        else:
            super().keyPressEvent(event)

class DisplayItem(QWidget):

    deleteButtonPressed=pyqtSignal(int)
    contentUpdateOccurred=pyqtSignal(int, str)

    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.m_data = data 

        self.m_layout = QVBoxLayout(self)
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.m_layout.setSpacing(0)

        title = self.m_data['title']
        content = self.m_data['content']
        color=self.m_data.get('color', None)

        self.title = QLabel(title)

        self.deleteButton=QPushButton()
        pixmapi = getattr(QStyle, 'SP_TrashIcon')
        icon = self.style().standardIcon(pixmapi)
        self.deleteButton.setIcon(icon)
        self.deleteButton.pressed.connect(self.on_deleteButtonPressed)

        self.info=QLabel(f'# {self.m_data.get("id")}')

        widget=QWidget()
        widget.m_layout=QHBoxLayout(widget)
        widget.m_layout.setContentsMargins(0,0,0,0)
        widget.m_layout.setSpacing(1)

        widget.m_layout.addWidget(self.info)
        widget.m_layout.addWidget(self.title)
        widget.m_layout.addStretch(1)
        widget.m_layout.addWidget(self.deleteButton)

        self.content = QTextEdit(content)
        self.content.adjustSize()
        self.content.textChanged.connect(self.on_contentChanged)


        if color:
            widget.setStyleSheet(f'background-color: {color}; color: black')
            self.content.setStyleSheet(f'background-color: {color}; color: black')

        self.m_layout.addWidget(widget)
        self.m_layout.addWidget(self.content)

        widget.adjustSize()
        self.content.adjustSize()

    def on_contentChanged(self):
        text=self.content.toPlainText()
        self.contentUpdateOccurred.emit(self.m_data['id'], text)

    def on_deleteButtonPressed(self):
        self.deleteButtonPressed.emit(self.m_data.get('id'))

    def sizeHint(self):
        size=self.content.size()
        size.setHeight(size.height()+20)
        return size 

    def adjustSize(self):
        self.content.adjustSize()
