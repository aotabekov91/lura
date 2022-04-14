import pathlib

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Display(QWidget):

    def __init__(self, parent, settings):
        super().__init__(parent.window)
        self.m_parent=parent
        self.window=parent.window
        self.s_settings=settings
        self.location='left'
        self.name='Notes'
        self.setup()

    def setup(self):

        self.m_layout=QVBoxLayout(self)
        self.m_layout.setContentsMargins(0, 0, 0, 0)

        self.activated=False
        self.window.setTabLocation(self, self.location, self.name)

    def open(self, n_id=None):
        if n_id is None:
            noteNumber=len(self.window.plugin.tables.getAll('notes'))
            title=f'Note_{noteNumber}'
            loc=f'{self.m_parent.baseFolder}/{title}.md'
            pathlib.Path(loc).touch()
            self.window.plugin.tables.write('notes', {'title':title, 'loc':loc})
            n_id=self.window.plugin.tables.get(
                    'notes', {'title':title, 'loc':loc}, 'id')

        noteWidget=NQWidget(n_id, self.window.plugin.tables)

        for i in reversed(range(self.m_layout.count())):
            self.m_layout.itemAt(i).widget().setParent(None)

        self.m_layout.addWidget(noteWidget)
        self.window.activateTabWidget(self)

    def toggle(self):

        if not self.activated:

            self.window.activateTabWidget(self)
            self.activated=True

        else:

            self.window.deactivateTabWidget(self)
            self.activated=False

class NQWidget(QWidget):

    def __init__(self, m_id, data):
        super().__init__()
        self.m_id=m_id
        self.m_data=data
        self.setup()

    def setup(self):

        self.m_layout=QVBoxLayout(self)
        self.m_layout.setContentsMargins(10, 10, 10, 10)

        widget=QWidget()
        widget.m_layout=QHBoxLayout(widget)
        widget.m_layout.setContentsMargins(0, 0, 0, 0)

        self.title=QLineEdit()
        self.title.textChanged.connect(self.on_titleChanged)

        self.saveButton=QPushButton('Save')
        self.saveButton.pressed.connect(self.on_saveButtonPressed)

        widget.m_layout.addWidget(self.title)
        widget.m_layout.addWidget(self.saveButton)
        
        self.content=QTextEdit()

        self.m_layout.addWidget(widget)
        self.m_layout.addWidget(self.content)

        note=self.m_data.get('notes', {'id':self.m_id})

        self.title.setText(note['title'])
        self.content.setPlainText(''.join(open(note['loc']).readlines()))

    def on_titleChanged(self, text):
        self.m_data.update('notes', {'id':self.m_id}, {'title':text})

    def on_saveButtonPressed(self):
        text=self.content.toPlainText()
        loc=self.m_data.get('notes', {'id':self.m_id}, 'loc')
        nFile=open(loc, 'w')
        for f in text:
            nFile.write(f)
