from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .base import BaseTreeWidget

class AnnotationTreeWidget(BaseTreeWidget):

    def setup(self):
        super().setup()
        self.toggleColor()

    def addSubFields(self):
        self.addContentField()
        self.addQuoteField()
        super().addSubFields()

class AnnotationProxyWidget(BaseTreeWidget):

    def setup(self):
        super().setup()
        self.toggleColor()
        self.toggle('content')
        self.toggle('tag')

        self.m_contentEdit.setFixedHeight(40)
        self.setFixedWidth(250)

    def addSubFields(self):
        self.addContentField()
        super().addSubFields()

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.hide()
        else:
            self.m_titleEdit.keyPressEvent(event)
