from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin

class Hint(Plugin):

    hintSelected=pyqtSignal(object, object)

    def __init__(self, app):

        super().__init__(app, listen_leader='f')

        self.trans=QTransform()
        self.app.window.display.pageHasBeenJustPainted.connect(self.paint)

    def listen(self):

        super().listen()

        self.hints=None
        self.selected_hint=None

        self.statusbar('Hint', kind='info')
        self.app.window.display.view.updateAll()
        self.app.manager.listen(self.app.window, self)

    def delisten(self):

        super().delisten()
        self.hints=None

        self.statusbar(kind='detail')
        self.statusbar(kind='info')

        self.app.window.display.view.updateAll()
        self.app.manager.delisten(self.app, self)

    def generate(self, hints):

        self.hints={}
        alphabet = 'abcdefghijklmnopqrstuvwxyz'

        len_of_codes = 2
        char_to_pos = {}
        for i in range(len(alphabet)):
            char_to_pos[alphabet[i]] = i

        def number_to_string(n):

            chars = []
            for _ in range(len_of_codes):
                chars.append(alphabet[n % len(alphabet)])
                n = n // len(alphabet)
            return "".join(reversed(chars))

        return {number_to_string(i): h for i, h in enumerate(hints)}

    def addKeys(self, text):

        if text: self.keys_pressed+=[text]

        key=f'{"".join(self.keys_pressed)}'
        self.statusbar(key, kind='edit')

        partial=self.findMatch(key)
        self.execute(key, partial)

    def execute(self, key, partial):

        if partial:
            if len(partial)==1:
                hint=partial[key]
                pageItem=self.app.window.display.view.pageItem()
                pageItem.setSelection([pageItem.mapToItem(hint.boundingBox())[0]])
                self.hintSelected.emit(pageItem, hint)
                self.delisten()
            else:
                self.hints=partial
                self.app.window.display.view.updateAll()
        else:
            self.keys_pressed=[]

    def findMatch(self, key): 

        hints={}
        for i, h in self.hints.items():
            if key in i: hints[i]=h
        return hints

    def paint(self, painter, options, widget, pageItem, view):

        if self.listening:

            painter.save()
            pen=QPen(Qt.red, 0.0)
            painter.setPen(pen)

            if not self.hints: self.hints=self.generate(pageItem.page().data().textList())

            for i, hint in self.hints.items():
                transformed_rect=pageItem.mapToItem(hint.boundingBox())[0]
                painter.drawText(transformed_rect.topLeft(), i)

            painter.restore()
