from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin
from lura.utils import classify

from lura.utils.widgets import SpecialKeyShortcut

class Jumper(Plugin):
    jumperAction=pyqtSignal(str)
    def __init__(self, app):
        super(Jumper, self).__init__(app)
        self.keys_pressed=[]
        self.app.window.installEventFilter(self)

    def listenDigits(self, event):
        if event.type()==QEvent.KeyPress:
            return event.text().isnumeric()
        else:
            return False

    def finishDigits(self, event):
        print(self.activated, self.listenDigits(event), event.type(), event.key())
        if self.activated:
            if hasattr(event, 'text'):
                if event.text().isnumeric():
                    return False
                else:
                    self.act(event)
                    return True

    def act(self, event):
        command=self.commandByKeys.get(event.text(), None)
        if command:
            func=getattr(self, command, None)
            if func:func()
        else:
            digitString=int(''.join(self.keys_pressed))
            typed='|'.join([digitString, event.text()])
            self.jumperAction.emit(typed)

    def gotoPage(self):
        if self.activated:
            page=int(''.join(self.keys_pressed))
            view=self.app.window.display.currentView()
            view.jumpToPage(page)

    def nextParagraph(self):
        pass

    def prevParagraph(self):
        pass

    def setShortcuts(self):
        self.commandByKeys={}
        if self.config:
            commands=dict(self.config.items())
            for command, key in commands.items():
                self.commandByKeys[key]=command

    def deactivate(self):
        super().deactivate()
        self.keys_pressed=[]

    def activate(self):
        super().activate(focus=False)
        self.keys_pressed=[]

    def updateStatusbar(self):
        if self.activated:
            digits=''.join(self.keys_pressed)
            self.app.window.statusBar().setDetailInfo(f'{self.name} [{digits}]')

    def eventFilter(self, widget, event):
        if self.activated: 
            if hasattr(event, 'text'):
                if self.finishDigits(event):
                    self.deactivate()
                else:
                    if event.type()==QEvent.KeyPress:
                        self.keys_pressed+=[event.text()]
        elif self.listenDigits(event):
            self.activate()
            self.keys_pressed+=[event.text()]
        self.updateStatusbar()
        return super().eventFilter(widget, event)
