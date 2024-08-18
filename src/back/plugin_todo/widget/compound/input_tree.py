from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..base import TreeWidget, InputLabelWidget

class InputTree (QWidget):

    hideWanted=pyqtSignal()
    returnPressed=pyqtSignal()
    inputTextChanged=pyqtSignal()
    inputReturnPressed=pyqtSignal()

    def __init__(self): 

        super(InputTree, self).__init__()

        layout, style_sheet=self.setUI()

        self.setLayout(layout)
        self.setStyleSheet(style_sheet)

        self.setMinimumSize(400, 600)

        self.input.hide()

    def setUI(self):

        style_sheet='''
            QWidget{
                font-size: 15px;
                color: white;
                border-width: 0px;
                background-color: #101010; 
                border-color: transparent;
                }
            QWidget#mainWidget{
                border-radius: 10px;
                border-style: outset;
                background-color: transparent; 
                }
                '''
        
        self.tree=TreeWidget()
        self.input=InputLabelWidget()

        self.tree.hideWanted.connect(self.hideWanted)

        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.input)
        layout.addWidget(self.tree)

        return layout, style_sheet

    def installEventFilter(self, treeener):

        self.tree.installEventFilter(treeener)
        self.input.installEventFilter(treeener)

    def setFocus(self): self.tree.setFocus()

    def toggleInput(self):

        if self.input.isVisible():
            self.input.hide()
            self.tree.setFocus()
        else:
            self.input.show()
            self.input.setFocus()

    def keyPressEvent(self, event):

        if event.modifiers() and  event.key() in [Qt.Key_BracketLeft]:
            self.hideWanted.emit()
        elif event.modifiers() and  event.key() in [Qt.Key_I]:
            self.toggleInput()
        else:
            super().keyPressEvent(event)
