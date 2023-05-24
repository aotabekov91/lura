from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin import ListWidget

from lura.utils import Plugin, watch
from lura.utils import BaseCommandStack

class Command(Plugin):

    def __init__(self, app):

        super(Command, self).__init__(app=app)

        self.setUI()
        self.update()

        self.app.installEventFilter(self)
        self.app.manager.pluginsLoaded.connect(self.update)

    def update(self): 

        self.dlist=sorted(self.app.manager.actions.values(), key=lambda x: x['plugin'])
        self.ui.main.setList(self.dlist, limit=None)

    def on_returnPressed(self):

        self.deactivate()
        item=self.ui.main.item(self.ui.main.currentRow())
        partial=[]
        key, digit = self.checkKeysPressed()

        if item and 'id' in item.itemData: partial=[item.itemData['id']]
        self.executeKeysPressed(partial, digit)

    def setUI(self):
        
        self.ui=BaseCommandStack(self, 'bottom')

        list_widget=ListWidget(check_fields=['down'], exact_match=True)

        self.ui.addWidget(list_widget, 'main', main=True)

        self.ui.hideWanted.connect(self.deactivate)
        self.ui.main.hideWanted.connect(self.deactivate)
        self.ui.main.returnPressed.connect(self.on_returnPressed)

        self.ui.installEventFilter(self)

    def activateListener(self): 

        super().activateListener()
        self.ui.activate()

    def deactivateListener(self): 

        super().deactivateListener()
        self.ui.main.unfilter()
        self.ui.deactivate()

    def findPartialKeysPressed(self, key, digit):

        self.ui.main.filter(key)
        partial=[]
        for i in range(self.ui.main.count()):
            partial+=[self.ui.main.item(i).itemData['id']]

        if len(partial)==1: 
            self.deactivate()
        elif len(partial)==0:
            self.ui.main.addItems([{'up': 'No match found'}])
        return partial

    def deactivateCommandMode(self):
        self.ui.main.unfilter()
        super().deactivateCommandMode()
        super().activateListener()

    def activateCommandMode(self):

        super().deactivateListener()
        super().activateCommandMode()

    def toggleCommandMode(self):

        if self.leader_activated:
            self.deactivateCommandMode()
        else:
            self.activateCommandMode()

    def eventFilter(self, widget, event):

        if self.listen and event.type()==QEvent.KeyPress:
            if event.key() in [Qt.Key_Enter, Qt.Key_Return]:
                self.on_returnPressed()
                return True
            elif event.key() in [Qt.Key_Backspace]:
                self.ui.main.setList(self.dlist)
                return True
            elif event.modifiers() and event.key() in [Qt.Key_N, Qt.Key_J]:
                self.ui.main.move(crement=1)
                return True
            elif event.modifiers() and event.key() in [Qt.Key_P, Qt.Key_K]:
                self.ui.main.move(crement=-1)
                return True
            elif event.text() in self.leader:
                self.toggleCommandMode()
                return True
        return super().eventFilter(widget, event)
