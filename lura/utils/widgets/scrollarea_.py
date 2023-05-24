from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Display(QWidget):

    keyPressEventOccurred=pyqtSignal(object)
    deleteButtonPressed=pyqtSignal(int)
    contentUpdateOccurred=pyqtSignal(int, str)
    filterChanged=pyqtSignal()

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
        self.setStyleSheet("background-color: black; color: white")

        self.scrollableWidget=QWidget()
        self.scrollableWidget.m_layout=QVBoxLayout(self.scrollableWidget)
        self.scrollableWidget.m_layout.setContentsMargins(0, 0, 0, 0)
        self.scrollableWidget.m_layout.setSpacing(3)

        self.scrollArea=QScrollArea()
        self.scrollArea.setWidget(self.scrollableWidget)
        self.scrollArea.setWidgetResizable(True)

        self.setFilter()
        self.m_layout.addWidget(self.filter)
        self.m_layout.addWidget(self.scrollArea)

        self.app.window.setTabLocation(self, self.location, self.name)

    def setFilter(self):
        if self.filter_kind=='combo':
            self.filter = QComboBox()
            self.filter.currentTextChanged.connect(self.filterChanged)
        elif self.filter_kind=='text':
            self.filter=QLineEdit()
            self.filter.textChanged.connect(self.filterChanged)

    def setFilterValues(self, values):
        if self.filter_kind=='combo':
            for value in values:
                self.filter.addItem(value)

    def keyPressEvent(self, event):
        self.keyPressEventOccurred.emit(event)

    def clear(self):
        for i in reversed(range(self.scrollableWidget.m_layout.count())):
            w=self.scrollableWidget.m_layout.itemAt(i).widget()
            self.scrollableWidget.m_layout.removeWidget(w)
            w.hide()

    def addItems(self, data, save=True):
        self.clear()
        if save: self.m_data=data

        for d in self.m_data:

            aWidget = DisplayItem(d)
            aWidget.contentUpdateOccurred.connect(self.contentUpdateOccurred)
            aWidget.deleteButtonPressed.connect(self.on_deleteButtonPressed)
            self.scrollableWidget.m_layout.addWidget(aWidget)

    def on_deleteButtonPressed(self, iid):
        self.deleteButtonPressed.emit(iid)
        raise

    def deactivate(self):
        self.app.window.deactivateTabWidget(self)

    def activate(self):
        self.app.window.activateTabWidget(self)
        self.setFocus()

class DisplayItem(QWidget):

    deleteButtonPressed=pyqtSignal(int)
    contentUpdateOccurred=pyqtSignal(int, str)

    def __init__(self, data):
        super().__init__()
        self.m_data = data 
        self.setup()

    def setup(self):
        self.m_layout = QVBoxLayout(self)
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.m_layout.setSpacing(0)

        title = self.m_data['title']
        content = self.m_data['content']

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
        self.content.setMinimumHeight(80)
        self.content.setMaximumHeight(140)
        self.content.textChanged.connect(self.on_contentChanged)

        color=self.m_data.get('color', None)

        if color:
            widget.setStyleSheet(f'background-color: {color}; color: black')
            self.content.setStyleSheet(f'background-color: {color}; color: black')

        self.m_layout.addWidget(widget)
        self.m_layout.addWidget(self.content)

    def on_contentChanged(self):
        text=self.content.toPlainText()
        self.contentUpdateOccurred.emit(self.m_data['id'], text)

    def on_deleteButtonPressed(self):
        self.deleteButtonPressed.emit(self.m_data.get('id'))
