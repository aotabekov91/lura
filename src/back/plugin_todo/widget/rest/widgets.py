from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..base import StackWindow, StackWidget
from ..base import UpDownEdit, LeftRightEdit
from ..base import InputLabelWidget, ListWidget, IconUpDown
from ..compound import InputListStack, CommandList, InputList

class InputListStackWindow(StackWindow):

    def __init__(self, window_name, 
                 label_name=None, 
                 item_class=IconUpDown,
                 list_class=ListWidget, 
                 input_class=InputLabelWidget,
                 input_list=None):
        self.label_name=label_name
        ui=self.setUI(item_class, list_class, input_class, input_list)
        super(InputListStackWindow, self).__init__(ui, window_name)

    def setUI(self, item_class, list_class, input_class, input_list):
        if input_list:
            ui=input_list(
                item_class=IconUpDown, 
                list_class=ListWidget, 
                input_class=InputLabelWidget)
        else:
            ui=InputListStack(
                    item_class=IconUpDown, 
                    list_class=ListWidget, 
                    input_class=InputLabelWidget)

        if self.label_name:
            ui.main.input.setLabel(self.label_name)

        return ui

    def ui(self):
        return self.stack

class CommandsStackWidget(StackWidget):
    def __init__(self, main_widget):
        super(CommandsStackWidget, self).__init__()
        self.addWidget(CommandList(), 'commands')
        if main_widget:
            self.setMainWidget(main_widget)

    def toggleCommands(self):
        if self.commands.isVisible():
            self.showMainWidget()
        else:
            self.setCurrentWidget(self.commands)

    def installEventFilter(self, listener):
        super().installEventFilter(listener)
        self.commands.setSource(listener)


class CommandsStackWindow(StackWindow):
    def __init__(self, main_widget=None, window_title=None):
        stack=CommandsStackWidget(main_widget)
        super(CommandsStackWindow, self).__init__(stack, window_title)

class InputEditList(InputList):
    contentChanged=pyqtSignal(object)
    def addItem(self, w):
        widget=super().addItem(w)
        widget.contentChanged.connect(self.contentChanged)
        return widget

class InputEditListWidget(InputList):

    contentChanged=pyqtSignal(object)

    def __init__(self):
        super(InputEditListWidget, self).__init__(
                item_class=LeftRightEdit,
                list_class=ListWidget,
                input_class=InputLabelWidget)

    def addItem(self, w):
        widget=super().addItem(w)
        widget.contentChanged.connect(self.contentChanged)
        return widget

class InputEditListStack(InputListStack):
    contentChanged=pyqtSignal(object)

    def __init__(self):
        super(InputEditListStack, self).__init__(
                item_class=LeftRightEdit, input_list=InputEditList)

    def addItem(self, w):
        widget=super().addItem(w)
        widget.contentChanged.connect(self.contentChanged)
        return widget

class InputListEditStackWindow(StackWindow):

    contentChanged=pyqtSignal(object)

    def __init__(self, window_title=None, label_title=None):
        super(InputListEditStackWindow, self).__init__(InputEditListStack(), window_title)
        if label_title: 
            self.ui().main.input.setLabel(label_title)
