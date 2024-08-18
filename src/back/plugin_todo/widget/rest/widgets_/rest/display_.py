from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.view.docviewer import DocumentView

class Display(QScrollArea):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent
        self.colorCode=settings['colorSystem']
        self.s_settings = settings
        self.location = 'right'
        self.name = 'Annotations'
        self.setup()

    def setup(self):

        self.m_view=None
        self.m_item=None

        self.group=QWidget()
        self.group.m_layout=QVBoxLayout(self.group)
        self.group.m_layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: black; color: white")

        self.colorCombo = QComboBox()
        for f in ['All']+list(self.colorCode.keys()):
            self.colorCombo.addItem(f)
        self.colorCombo.setCurrentText('All')
        self.colorCombo.currentTextChanged.connect(self.on_colorComboChanged)

        self.scrollableWidget=QWidget()
        self.scrollableWidget.m_layout=QVBoxLayout(self.scrollableWidget)
        self.scrollableWidget.m_layout.setContentsMargins(0, 0, 0, 0)
        self.scrollableWidget.m_layout.setSpacing(3)

        self.group.m_layout.addWidget(self.colorCombo)
        self.group.m_layout.addWidget(self.scrollableWidget)
        self.group.m_layout.addStretch(1)

        self.window.viewChanged.connect(self.on_viewChanged)
        self.window.mapItemChanged.connect(self.on_mapItemChanged)

        self.window.setTabLocation(self, self.location, self.name)

        if type(self.m_view)==DocumentView:
            self.load(self.m_view.document().id())
        elif self.m_item is not None:
            if self.m_item.kind()!='document': return
            self.load(self.m_item.id())
        else:
            view=self.window.view()
            if view is None: return
            self.load(view.document().id())

    def on_mapItemChanged(self, item):

        if not self.isVisible(): return
        if item is None or item.kind()!='document': return
        if self.m_item and self.m_item==item: return
            
        self.m_item=item
        self.m_view=None
        self.load(item.id())

    def on_viewChanged(self, view):

        if not self.isVisible(): return
        if view is None: return
        if self.m_view==view: return

        self.m_view=view
        self.m_item=None
        if type(view)==DocumentView:
            self.load(view.document().id())
        else:
            item=view.currentItem()
            if item is None or item.kind()!='document': return
            self.load(item.id())

    def load(self, did=None, function=None):

        if did is None: 
            if self.window.view() is None: return
            did=self.window.view().document().id()

        if function is None:
            function = self.colorCombo.currentText()

        for i in reversed(range(self.scrollableWidget.m_layout.count())):
            w=self.scrollableWidget.m_layout.itemAt(i).widget()
            self.scrollableWidget.m_layout.removeWidget(w)
            w.hide()

        criteria={'did':did}
        if function is not None and function!='All':
            criteria['color']=self.colorCode[function]

        annotations = self.window.plugin.tables.get(
                'annotations', criteria, unique=False)

        if annotations is None: return

        self.m_annotations = sorted(
            annotations,
            key=lambda d: (d['page'], d['position'].split(':')[1])
        )

        for annotation in self.m_annotations:

            aWidget = AQWidget(annotation['id'], self.window)
            self.scrollableWidget.m_layout.addWidget(aWidget)

        self.setWidget(self.group)
        self.setWidgetResizable(True)

    def update(self):
        for i in reversed(range(self.scrollableWidget.m_layout.count())):
            self.scrollableWidget.m_layout.itemAt(i).widget().update()

    def toggle(self):

        if not self.isVisible():

            self.window.activateTabWidget(self)
            self.load()
            self.setFocus()

        else:

            self.window.deactivateTabWidget(self)
            view=self.window.view()
            if view is None: return
            view.setFocus()
    def keyPressEvent(self, event):
        if event.key()==Qt.Key_F:
            self.colorCombo.setCurrentText('Definition')
        elif event.key()==Qt.Key_A:
            self.colorCombo.setCurrentText('All')
        elif event.key()==Qt.Key_M:
            self.colorCombo.setCurrentText('Main')
        elif event.key()==Qt.Key_D:
            self.colorCombo.setCurrentText('Data')
        elif event.key()==Qt.Key_N:
            self.colorCombo.setCurrentText('Question')
        elif event.key()==Qt.Key_R:
            self.colorCombo.setCurrentText('Source')


class AQWidget(QWidget):

    def __init__(self, aid, window):
        super().__init__()
        self.m_id = aid
        self.m_window=window
        self.m_data = window.plugin.tables
        self.setup()

    def setup(self):
        self.m_layout = QVBoxLayout(self)
        self.m_layout.setContentsMargins(0, 0, 0, 0)
        self.m_layout.setSpacing(0)

        title = self.m_data.get('annotations', {'id': self.m_id}, 'title')
        content = self.m_data.get('annotations', {'id': self.m_id}, 'content')

        self.title = QLineEdit(title)
        self.title.setFixedHeight(25)
        self.title.textChanged.connect(self.on_titleChanged)
        self.title.mouseDoubleClickEvent=self.on_titleDoubleClick

        self.deleteButton=QPushButton()
        pixmapi = getattr(QStyle, 'SP_TrashIcon')
        icon = self.style().standardIcon(pixmapi)
        self.deleteButton.setIcon(icon)
        self.deleteButton.pressed.connect(self.on_deleteButtonPressed)

        self.info=QLabel(f'{self.m_id}')

        widget=QWidget()
        widget.m_layout=QHBoxLayout(widget)
        widget.m_layout.setContentsMargins(0,0,0,0)
        widget.m_layout.setSpacing(1)

        widget.m_layout.addWidget(self.title)
        widget.m_layout.addWidget(self.deleteButton)
        widget.m_layout.addWidget(self.info)

        self.content = QTextEdit(content)
        self.content.setMinimumHeight(80)
        self.content.setMaximumHeight(140)
        self.content.textChanged.connect(self.on_contentChanged)

        color=self.m_data.get('annotations', {'id': self.m_id}, 'color')
        if color is not None:
            widget.setStyleSheet(f'background-color: {color}; color: black')
            self.content.setStyleSheet(f'background-color: {color}; color: black')

        self.m_layout.addWidget(widget)
        self.m_layout.addWidget(self.content)
        # self.m_layout.addWidget(self.deleteButton)

    def update(self):
        self.title.setText(
                self.m_data.get('annotations', {'id': self.m_id}, 'title'))
        self.content.setPlainText(
                self.m_data.get('annotations', {'id': self.m_id}, 'content'))

    def on_titleDoubleClick(self, event):
        aData=self.m_data.get('annotations', {'id':self.m_id})
        pageNumber=aData['page']

        b=aData['position'].split(':')
        topLeft=QPointF(float(b[0]), float(b[1]))

        self.m_window.view().jumpToPage(
                pageNumber, topLeft.x(), .95*topLeft.y())


    def on_titleChanged(self, text):
        self.m_data.update('annotations', {'id':self.m_id}, {'title':text})

    def on_contentChanged(self):
        text=self.content.toPlainText()
        self.m_data.update('annotations', {'id':self.m_id}, {'content':text})

    def on_deleteButtonPressed(self):
        self.m_window.plugin.annotation.remove(self.m_id)
