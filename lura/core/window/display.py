from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Display(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setup()

    def setup(self):
        self.m_layout=QVBoxLayout(self)
        self.m_layout.setSpacing(0)
        self.m_layout.setContentsMargins(0,0,0,0)

    def clear(self):
        for index in range(self.m_layout.count()):
            item=self.m_layout.takeAt(index)
            if item: item.widget().hide()

    def setView(self, view):
        self.clear()
        self.m_layout.addWidget(view)
        view.show()

    def removeView(self, view):
        self.m_layout.removeWidget(view)

    def addView(self, view):
        self.m_layout.addWidget(view)

    def focusView(self):
        self.show()
        if self.m_layout.count()>0:
            view=self.m_layout.itemAt(0).widget()
            view.setFocus()
            return view
