from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

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

        self.group=QWidget()
        self.group.m_layout=QVBoxLayout(self.group)
        self.group.m_layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("background-color: black; color: white")

        self.colorCombo = QComboBox()
        for f in ['All', 'Main', 'Definition', 'Question', 'Source']:
            self.colorCombo.addItem(f)
        self.colorCombo.setCurrentText('All')
        self.colorCombo.currentTextChanged.connect(self.on_colorComboChanged)

        self.scrollableWidget=QWidget()
        self.scrollableWidget.m_layout=QVBoxLayout(self.scrollableWidget)
        self.scrollableWidget.m_layout.setContentsMargins(0, 0, 0, 0)

        self.group.m_layout.addWidget(self.colorCombo)
        self.group.m_layout.addWidget(self.scrollableWidget)
        self.group.m_layout.addStretch(1)

        self.window.viewChanged.connect(self.on_viewChanged)
        self.window.setTabLocation(self, self.location, self.name)

    def on_colorComboChanged(self):
        function = self.colorCombo.currentText()
        self.load(self.window.view().document(), function)

    def on_viewChanged(self, view):

        self.load(view.document())

    def load(self, document=None, function=None):

        if document is None: document=self.window.view().document()

        for i in reversed(range(self.scrollableWidget.m_layout.count())):
            self.scrollableWidget.m_layout.itemAt(i).widget().setParent(None)

        criteria={'did':document.id()}
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

        if self.window.view() is None: return

        if not self.isVisible():

            self.window.activateTabWidget(self)

        else:

            self.window.deactivateTabWidget(self)
            self.window.view().setFocus()


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

        self.content = QTextEdit(content)
        self.content.setMinimumHeight(80)
        self.content.setMaximumHeight(140)
        self.content.textChanged.connect(self.on_contentChanged)

        color=self.m_data.get('annotations', {'id': self.m_id}, 'color')
        if color is not None:
            self.title.setStyleSheet(f'background-color: {color}; color: black')
            self.content.setStyleSheet(f'background-color: {color}; color: black')

        self.m_layout.addWidget(self.title)
        self.m_layout.addWidget(self.content)

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
