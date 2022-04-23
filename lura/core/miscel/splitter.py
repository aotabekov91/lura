from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class DisplaySplitter(QSplitter):

    def __init__(self):
        super().__init__(Qt.Vertical)
        self.setup()

    def setup(self):

        self.m_layout=QVBoxLayout(self)

        self.m_layout.setSpacing(0)
        self.m_layout.setContentsMargins(0,0,0,0)

    def clear(self):
        for index in range(self.m_layout.count()):
            item=self.m_layout.takeAt(index)
            item.widget().hide()

    def setWidget(self, widget):

        self.clear()
        self.m_layout.addWidget(widget)

    def removeWidget(self, widget):

        self.m_layout.removeWidget(widget)

    def addWidget(self, widget):
        self.m_layout.addWidget(widget)

    def replaceWidget(self, index, widget):

        if self.m_layout.count()>0:
            self.m_layout.insertWidget(index, widget)
            self.m_layout.takeAt(index+1)
        else:
            self.m_layout.addWidget(widget)

    def focusDocumentView(self):
        self.show()
        if self.m_layout.count()>0:
            view=self.m_layout.itemAt(0).widget()
            view.setFocus()
            return view
