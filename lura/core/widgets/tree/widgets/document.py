from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .base import BaseTreeWidget

class DocumentTreeWidget(BaseTreeWidget):

    def setup(self):
        super().setup()

    def addSubFields(self):
        self.addAuthorField()
        super().addSubFields()
