from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from notes import _get_definition 
from lura.core.widgets import CustomTree

class Pager(QWidget):

    def __init__(self, parent, settings):
        super().__init__()
        self.window=parent
        self.s_settings=settings
        self.name = 'pager'
        self.globalKeys={
                'Ctrl+g': (
                    self.toggle,
                    self.window,
                    Qt.WindowShortcut)
                }
        self.setup()

    def setup(self):

        self.activated=False
        self.m_edit=QLineEdit()
        self.m_edit.returnPressed.connect(self.jumpToPage)
        self.m_edit.setFixedWidth(40)
        self.m_total=QLabel()
        self.m_label=QLabel()

        layout=QGridLayout(self)
        layout.addWidget(self.m_label, 0, 0, 1, 15)
        layout.addWidget(self.m_edit, 0, 16, 1, 1)
        layout.addWidget(self.m_total, 0, 17, 1, 1)

    def jumpToPage(self):
        self.toggle()
        try:
            page=int(self.m_edit.text())
            self.window.view().jumpToPage(page)
        except:
            pass

    def populateData(self):

        self.m_label.setText(self.window.view().document().title())
        self.m_edit.setText(str(self.window.view().currentPage()))
        self.m_total.setText('/'+str(self.window.view().totalPages()))

    def toggle(self):

        if self.window.view() is None: return

        if not self.activated: 

            self.activated=True
            self.populateData()
            self.window.activateStatusBar(self)
            self.m_edit.setFocus()

        else:

            self.window.deactivateStatusBar(self)
            self.activated=False

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.toggle()
        else:
            super().keyPressEvent(event)
