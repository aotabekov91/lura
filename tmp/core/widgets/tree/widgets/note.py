from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .base import BaseTreeWidget

class NoteTreeWidget(BaseTreeWidget):

    def setup(self):
        super().setup()
        self.toggleColor()

    def addSubFields(self):
        self.addContentField()
        super().addSubFields()
