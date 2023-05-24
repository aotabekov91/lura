from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin, register

class BookmarkCreator(Plugin):

    def __init__(self, app): 

        super().__init__(app, name='bookmark', mode_keys={'command': 'b'})

    @register('b', modes=['normal', 'command'])
    def activate(self):

        view=self.app.window.display.currentView()
        if view:
            self.activated=True

            self.app.modes.plug.setClient(self)
            self.app.modes.setMode('plug')

            self.app.window.bar.show()
            self.app.window.bar.edit.setFocus()
            self.app.window.bar.edit.returnPressed.connect(self.add)
            self.app.window.bar.hideWanted.connect(self.deactivate)

            data=self.get()
            if data: self.app.window.bar.edit.setText(data[0]['text'])

    def deactivate(self):

        self.activated=False

        self.app.modes.setMode()
        self.app.modes.plug.setClient()

        self.app.window.bar.hide()
        self.app.window.bar.edit.returnPressed.disconnect(self.add)
        self.app.window.bar.hideWanted.disconnect(self.deactivate)

    def get(self):

        view=self.app.window.display.currentView()
        if view:
            data={}
            data['hash']=view.document().hash()
            data['page']=view.pageItem().page().pageNumber()
            data['position']=':'.join([str(f) for f in view.saveLeftAndTop()])
            return self.app.tables.bookmark.getRow(data)

    def add(self):

        text=self.app.window.bar.edit.text()
        self.deactivate()

        view=self.app.window.display.currentView()

        if view:
            data=self.get()
            if data:
                bid=data[0]['id']
                self.app.tables.bookmark.updateRow(
                        {'id':bid}, {'text':text})
            else:
                data={}
                data['text']=text
                data['kind']='document'
                data['hash']=view.document().hash()
                data['page']=view.pageItem().page().pageNumber()
                data['position']=':'.join([str(f) for f in view.saveLeftAndTop()])
                self.app.tables.bookmark.writeRow(data)
