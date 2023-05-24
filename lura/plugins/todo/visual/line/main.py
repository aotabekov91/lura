from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin

class WordHint(Plugin):

    def __init__(self, app):

        super().__init__(app)

        self.activated=True
        self.hint_words=False

        self.app.window.display.pageHasBeenJustPainted.connect(self.paintLinks)
        self.app.window.installEventFilter(self)

        self.trans=QTransform()

    def activateWordHint(self):

        self.keys_pressed=[]
        self.hint_words=True
        self.app.window.bar.detail.setText('')
        self.app.window.bar.info.setText('[Visual] Hint word')
        self.app.window.display.view.updateAll()

    def deactivateWordHint(self):

        self.keys_pressed=[]
        self.hint_words=False
        self.app.window.bar.detail.setText('')
        self.app.window.bar.info.setText('[Visual]')
        self.app.window.display.view.updateAll()

    def toggleWordHint(self):

        if not self.hint_words:
            self.activateWordHint()
        else:
            self.deactivateWordHint()

    def activateListener(self): 

        super().activateListener()
        self.app.window.bar.info.setText('[Visual]')
        self.app.window.bar.info.show()
        self.app.window.bar.show()

    def deactivateListener(self): 

        super().deactivateListener()

        self.app.window.bar.info.setText('')
        self.app.window.bar.info.hide()
        self.app.window.bar.hide()

        if self.hint_words: self.deactivateWordHint()

    def executeKeysPressed(self, *args, **kwargs):

        kwargs.pop('deactivate_listener', None)
        super().executeKeysPressed(*args, **kwargs, deactivate_listener=False)

    def eventFilter(self, widget, event):

        if self.listen and event.type()==QEvent.KeyPress:

            if event.key() in [Qt.Key_Backspace]:
                self.keys_pressed=[]
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

    def paintLinks(self, painter, options, widget, pageItem, view):

        if self.activated:

            if self.hint_words:

                hints=pageItem.page().data().textList()
                size=pageItem.page().data().pageSizeF()
                self.trans.reset()
                self.trans.scale(1/size.width(), 1/size.height())
                painter.save()
                painter.setTransform(pageItem.m_normalizedTransform, True)
                painter.setPen(QPen(Qt.red, 0.0))
                for hint in hints: painter.drawRect(self.trans.mapRect(hint.boundingBox()))
                painter.restore()
