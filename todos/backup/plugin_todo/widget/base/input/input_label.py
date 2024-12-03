from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .input import InputWidget

class InputLabelWidget (QWidget):

    hideWanted=pyqtSignal()
    textChanged=pyqtSignal()
    returnPressed=pyqtSignal()

    def __init__ (self, *args, **kwargs): 

        super().__init__(*args, **kwargs) 
        self.setUI()

    def setUI(self):

        self.style_sheet='''
            QWidget{
                color: black;
                background-color: white;
                border-color: red;
                border-width: 2px;
                border-radius: 10px;
                border-style: outset;
                }
            #label{
                border-color: transparent;
                border-width: 0px;
                padding: 0px 5px 0px 10px;
                border-radius: 10px;
                border-style: outset;
                }
                '''

        self.m_label= QLabel(objectName='label')

        layout=QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.m_label)

        self.m_input_label=QWidget(objectName='label')
        self.m_input_label.setLayout(layout)

        self.m_edit=InputWidget(self, objectName='label')
        self.m_edit.setStyleSheet(self.style_sheet)

        layout=QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.m_edit)

        self.m_input_edit=QWidget(self, objectName='label')
        self.m_input_edit.setLayout(layout)

        layout  = QHBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(3,3,3,3)
        layout.addWidget(self.m_input_label, 10)
        layout.addWidget(self.m_input_edit, 90)

        self.m_container=QWidget(objectName='inputContainerInput')
        self.m_container.setLayout(layout)

        layout=QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.m_container)

        self.setLayout(layout)
        self.setStyleSheet(self.style_sheet)

        self.m_edit.textChanged.connect(self.textChanged)
        self.m_edit.returnPressed.connect(self.returnPressed)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setFixedHeight(50)

        self.adjustSize()

    def adjustSize(self):

        self.m_edit.adjustSize()
        super().adjustSize()

    def hideLabel(self):

        self.m_label.hide()
        self.m_input_label.hide()

    def showLabel(self):

        self.m_label.show()
        self.m_input_label.show()

    def installEventFilter(self, listener): self.m_edit.installEventFilter(listener)

    def removeEventFilter(self, listener): self.m_edit.removeEventFilter(listener)

    def label(self): return self.m_label.text()

    def setLabel(self, label):

        self.m_label.setText(label)
        self.m_label.setAlignment(Qt.AlignCenter)
        self.showLabel()

    def text(self): return self.m_edit.text()

    def setText(self, text): self.m_edit.setText(text)

    def clear(self): self.m_edit.clear()

    def setFocus(self): self.m_edit.setFocus()

    def keyPressEvent(self, event):
        if event.modifiers() and event.key() in [Qt.Key_BracketLeft]:
            self.hideWanted.emit()
        super().keyPressEvent(event)
