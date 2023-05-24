from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class SpecialKeyShortcut(QObject):

    activated=pyqtSignal(list)

    def __init__(self, parent=None, specialKey=None, key=None):
        super(SpecialKeyShortcut, self).__init__()
        self._activated=False
        self._pressed=[]
        self._activator=specialKey
        self.setActivatorFilter()
        self.setFinishFilter()
        self.setWidget(parent)

    def setFinishFilter(self, filter=None):
        def unitLength(event):
            return len(self._pressed)==1

        self._finish=filter
        if not self._finish:
            self._finish=unitLength

    def setActivatorFilter(self, filter=None):
        def textMatch(event):
            return self._activator==event.key()

        self._start=filter
        if not self._start:
            self._start=textMatch

    def setSpecialKey(self, specialKey):
        self._activator=specialKey

    def setKey(self, key):
        self._key=key

    def setWidget(self, parent):
        self._parent=parent
        if self._parent:
            self._parent.installEventFilter(self)

    def eventFilter(self, widget, event):
        if event.type()==QEvent.KeyPress:
            if self._start(event):
                self._activated=True
                self._pressed+=[event.text()]
            elif self._activated: 
                self._pressed+=[event.text()]
                if self._finish(event):
                    self._activated=False
                    self.activated.emit(self._pressed)
                    self._pressed=[]
        return super().eventFilter(widget, event)
