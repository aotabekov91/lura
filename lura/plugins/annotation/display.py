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

        self.activated = False

        
        self.group=QWidget()
        self.group.m_layout=QVBoxLayout(self.group)

        self.colorCombo = QComboBox()
        for f in ['All', 'Main', 'Definition', 'Question', 'Source']:
            self.colorCombo.addItem(f)
        self.colorCombo.currentTextChanged.connect(self.on_colorComboChanged)

        self.scrollableWidget=QWidget()
        self.scrollableWidget.m_layout=QVBoxLayout(self.scrollableWidget)

        self.scrollableWidget.m_layout.setContentsMargins(0, 0, 0, 0)

        self.group.m_layout.addWidget(self.colorCombo)
        self.group.m_layout.addWidget(self.scrollableWidget)
        self.group.m_layout.addStretch(1)

        self.group.m_layout.setContentsMargins(0, 0, 0, 0)

        self.window.viewChanged.connect(self.on_viewChanged)
        self.window.setTabLocation(self, self.location, self.name)

    def on_colorComboChanged(self):
        function = self.colorCombo.currentText()
        self.update(self.window.view().document(), function)

    def on_viewChanged(self, view):

        self.update(view.document())

    def update(self, document, function='All'):

        for i in reversed(range(self.scrollableWidget.m_layout.count())):
            self.scrollableWidget.m_layout.itemAt(i).widget().setParent(None)

        criteria={'did':document.id()}
        if function!='All':
            criteria['color']=self.colorCode[function]

        annotations = self.window.plugin.tables.get(
            'annotations', criteria, unique=False)

        if annotations is None: return

        self.m_annotations = sorted(
            annotations,
            key=lambda d: (d['page'], d['position'].split(':')[1])
        )

        for annotation in self.m_annotations:

            aWidget = AQWidget(annotation['id'], self.window.plugin.tables)
            self.scrollableWidget.m_layout.addWidget(aWidget)


        self.setWidget(self.group)
        self.setWidgetResizable(True)

    def toggle(self):

        if self.window.view() is None:
            return

        if not self.activated:

            self.window.activateTabWidget(self)
            self.activated = True

        else:

            self.window.deactivateTabWidget(self)
            self.window.view().setFocus()
            self.activated = False


class AQWidget(QWidget):

    def __init__(self, aid, data):
        super().__init__()
        self.m_id = aid
        self.m_data = data
        self.setup()

    def setup(self):
        self.layout = QVBoxLayout(self)

        title = self.m_data.get('annotations', {'id': self.m_id}, 'title')
        content = self.m_data.get('annotations', {'id': self.m_id}, 'content')

        self.title = QLineEdit(title)
        self.title.setFixedHeight(25)
        self.title.textChanged.connect(self.on_titleChanged)

        self.content = QTextEdit(content)
        self.content.setMinimumHeight(80)
        self.content.setMaximumHeight(140)
        self.content.textChanged.connect(self.on_contentChanged)

        color=self.m_data.get('annotations', {'id': self.m_id}, 'color')
        if color is not None:
            self.title.setStyleSheet(f'background-color: {color}')
            self.content.setStyleSheet(f'background-color: {color}')

        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.content)

    def on_titleChanged(self, text):
        self.m_data.update('annotations', {'id':self.m_id}, {'title':text})

    def on_contentChanged(self):
        text=self.content.toPlainText()
        self.m_data.update('annotations', {'id':self.m_id}, {'content':text})
