from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin

# from .word_hint import WordHint

class Visual(Plugin):

    def __init__(self, app):

        super().__init__(app)

        # self.word_hint=WordHint(app)

    def toggleWordHint(self): self.word_hint.toggle()

    def listen(self): 

        super().listen()
        self.statusbar('[Visual]', kind='info')

    def delisten(self): 

        super().delisten()
        self.app.manager.listen(self, self.app)
        self.statusbar(kind='info')

        # self.word_hint.deactivate()

    def execute(self, partial, digit=None, deactivate_listener=True): 

        super().execute(partial, digit, False)

    def eventFilter(self, widget, event):

        if self.listening and event.type()==QEvent.KeyPress:
            if event.key() in [Qt.Key_Backspace]:
                self.listen()
                return True
        return super().eventFilter(widget, event)
