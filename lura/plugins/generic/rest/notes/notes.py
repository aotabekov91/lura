import os
import pathlib

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .display import Display

from .table import NotesTable
from lura.core.miscel import *

class Notes(MapTree):

    def __init__(self, parent, settings):
        super().__init__(parent, parent)
        self.window=parent
        self.display=Display(self, settings)
        self.baseFolder=settings['baseFolder']
        self.name = 'notes'
        self.location='left'
        self.globalKeys={
                'Ctrl+n': (
                    self.showNotes,
                    self.window,
                    Qt.WindowShortcut),
                'Ctrl+Shift+n': (
                    self.display.toggle,
                    self.window,
                    Qt.WindowShortcut),
                    }

        self.setup()

    def setup(self):
        self.window.plugin.tables.addTable(NotesTable)
        self.window.setTabLocation(self, self.location, self.name)

    def showNotes(self):

        notes=self.window.plugin.tables.get('notes')

        model=ItemModel()
        model.itemChanged.connect(self.on_itemChanged)

        for n in notes:
            item=Item('note', n['id'], self.window, n['title'])
            model.appendRow(item)

        self.setModel(model)
        self.window.activateTabWidget(self)
        self.setFocus()

    def open(self):
        item=self.currentItem()
        if item is None: return

        if pathlib.Path(item.get('loc')).exists():
            self.close()
            self.display.open(item.id())
        else:
            self.delete()

    def delete(self):
        item=self.currentItem()
        if item is None: return

        loc=item.get('loc')
        if pathlib.Path(loc).exists(): os.remove(loc)

        self.window.plugin.tables.remove('notes', {'id': item.id()})
        self.model().invisibleRootItem().takeRow(item.row())

    def on_itemChanged(self, item):
        self.window.plugin.tables.update(
                'notes', {'id':item.id()}, {'title':item.text()})
        path=item.get('title').lower().replace(' ', '_')
        loc=item.get('loc').rsplit('/', 1)[0]

        if not path.lower().endswith('md'):
            loc=f'{loc}/{path}.md'
        else:
            loc=f'{loc}/{path}'

        os.rename(item.get('loc'), loc)
        self.window.plugin.tables.update(
                'notes', {'id':item.id()}, {'loc':loc})

    def addNode(self):
        
        noteNumber=len(self.window.plugin.tables.get('notes'))
        title=f'Note_{noteNumber}'
        path=title.lower().replace(' ', '_')
        loc=f'{self.baseFolder}/{path}.md'
        pathlib.Path(loc).touch()
        self.window.plugin.tables.write('notes', {'title':title, 'loc':loc})
        n_id=self.window.plugin.tables.get(
                'notes', {'title':title, 'loc':loc}, 'id')
        item=Item('note', n_id, self.window, title)
        self.model().appendRow(item)
        self.setCurrentIndex(item.index())

    def watch(self):

        qIterator = QDirIterator(
            self.baseFolder, ["*.md", "*.MD"], QDir.Files, QDirIterator.Subdirectories)

        while qIterator.hasNext():
            loc=qIterator.next()
            data=self.window.plugin.tables.get(
                    'notes', {'loc':loc}, 'id')
            if data is not None: continue

            title=loc.rsplit('/', 1)[1]
            self.window.plugin.tables.write(
                    'notes', {'loc':loc, 'title':title})
                
        notes=self.window.plugin.tables.get('notes')

        for n in notes:
            if pathlib.Path(n['loc']).exists: continue
            self.window.plugin.tables.remove(
                    'notes', {'id': n['id']})

    def close(self):
        self.window.deactivateTabWidget(self)
