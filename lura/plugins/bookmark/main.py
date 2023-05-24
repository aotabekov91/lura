import os

from tables import Bookmark as Table
from plugin.widget import UpDownEdit, InputList

from lura.utils import Plugin, register
from lura.utils import getPosition, getBoundaries, BaseInputListStack

class Bookmark(Plugin):

    def __init__(self, app):

        super().__init__(app,
                         position='right',
                         mode_keys={'command':'b'},
                         bar_data={'edit': ''},
                         ) 

        self.app.tables.add_table(Table, 'bookmark')

        self.setUI()

    def setUI(self):

        super().setUI()

        main=InputList(item_widget=UpDownEdit)

        self.ui.addWidget(main, 'main', main=True)
        self.ui.main.input.hideLabel()
        self.ui.main.returnPressed.connect(self.open)
        self.ui.main.list.widgetDataChanged.connect(self.on_contentChanged)

        self.ui.hideWanted.connect(self.deactivateDisplay)
        self.ui.installEventFilter(self)

    @register('o')
    def open(self):

        item=self.ui.main.list.currentItem()
        dhash=item.itemData['hash']
        page=item.itemData['page']
        x, y=(float(i) for i in item.itemData['position'].split(':'))
        data=self.app.tables.hash.getPath(dhash)

        view=self.app.window.display.currentView()
        if view and view.document():
            if dhash!=view.document().hash():
                path=self.app.tables.hash.getPath(dhash)
                if os.path.exists(path): self.app.window.open(path, how='reset')

        view=self.app.window.display.currentView()
        if view: view.jumpToPage(page, x, y-0.4)

        self.ui.show()

    def on_contentChanged(self, widget):

        bid=widget.data['id']
        text=widget.data['down']
        self.app.tables.bookmark.updateRow({'id':bid}, {'text':text})

    @register('O')
    def openAndHide(self): 

        self.open()
        self.deactivateDisplay()

    @register('D')
    def delete(self):

        item=self.ui.main.list.currentItem()
        nrow=self.ui.main.list.currentRow()-1
        bid=item.itemData['id']
        self.app.tables.bookmark.removeRow({'id':bid})
        self.updateData()
        self.ui.main.list.setCurrentRow(nrow)
        self.ui.show()

    @register('u')
    def updateData(self, view=None):

        if not view: view=self.app.window.display.currentView()

        if view:
            criteria={'hash': view.document().hash()}
            self.bookmarks = self.app.tables.bookmark.getRow(criteria)
            if self.bookmarks:
                for a in self.bookmarks:
                    a['up']=f'# {a.get("id")}'
                    a['down']=a['text']
            self.bookmarks=sorted(self.bookmarks, key=lambda x: (x['page'], x['position']))
            self.ui.main.setList(self.bookmarks)

    @register('a')
    def activateDisplay(self):

        self.activated=True

        self.app.modes.plug.setClient(self)
        self.app.modes.setMode('plug')

        self.updateData()
        self.ui.activate()

    @register('a')
    def deactivateDisplay(self):

        self.activated=False

        self.app.modes.plug.setClient()
        self.app.modes.setMode('normal')

        self.ui.deactivate()

    @register('t')
    def toggle(self): 

        if self.activated:
            self.deactivateDisplay()
        else:
            self.activateDisplay()

    @register('b', modes=['normal', 'command'])
    def bookmark(self):

        view=self.app.window.display.currentView()
        if view:
            self.activated=True

            self.app.modes.plug.setClient(self)
            self.app.modes.setMode('plug')

            self.app.window.bar.show()
            self.app.window.bar.edit.setFocus()
            self.app.window.bar.edit.returnPressed.connect(self.writeBookmark)
            self.app.window.bar.hideWanted.connect(self.deactivate)

            data=self.getBookmark()
            if data: self.app.window.bar.edit.setText(data[0]['text'])

    def deactivate(self):

        self.activated=False

        self.app.modes.plug.setClient()
        self.app.modes.setMode('normal')

        self.app.window.bar.hide()

        self.app.window.bar.edit.returnPressed.disconnect(self.writeBookmark)
        self.app.window.bar.hideWanted.disconnect(self.deactivate)

    def getBookmark(self):

        view=self.app.window.display.currentView()
        if view:
            data={}
            data['hash']=view.document().hash()
            data['page']=view.pageItem().page().pageNumber()
            data['position']=':'.join([str(f) for f in view.saveLeftAndTop()])
            return self.app.tables.bookmark.getRow(data)

    def writeBookmark(self):

        text=self.app.window.bar.edit.text()
        self.deactivate()

        view=self.app.window.display.currentView()

        if view:
            data=self.getBookmark()
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
