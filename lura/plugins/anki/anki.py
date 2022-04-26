from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from anki.storage import Collection

from .table import AnkiNote
from lura.core.miscel import *

class Anki(QWidget):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent
        self.s_settings=settings
        self.db=AnkiNote(self.window)
        self.name = 'Anki'
        self.location='right'
        self.globalKeys={
                'Ctrl+a': (
                    self.toggle, 
                    self.window,
                    Qt.WindowShortcut,
                    ), 
                }

        self.mediaFolder = '/home/adam/.local/share/Anki2/kim/collection.media/'

        self.setup()

    def collection(self):
        return Collection('/home/adam/.local/share/Anki2/kim/collection.anki2')

    def setup(self):

        self.activated=False
        self.m_fields=[]

        self.setAnkiData()

        self.deckWidget=QComboBox()
        self.deckWidget.addItems(self.decks)
        self.deckWidget.currentTextChanged.connect(self.on_deckChanged)
        self.modelWidget=QComboBox()
        self.modelWidget.addItems(self.models)
        self.modelWidget.currentTextChanged.connect(self.on_modelChanged)
        self.fieldWidget=QWidget()
        self.save=QPushButton('Save')
        self.save.pressed.connect(self.on_savePressed)

        self.m_layout=QVBoxLayout(self)
        self.m_fieldLayout=QVBoxLayout(self.fieldWidget)
        self.m_fieldLayout.setContentsMargins(0,0,0,0)
        self.m_fieldLayout.setSpacing(0)

        self.m_layout.addWidget(self.deckWidget)
        self.m_layout.addWidget(self.modelWidget)
        self.m_layout.addWidget(self.fieldWidget)
        self.m_layout.addWidget(self.save)

        self.m_layout.addStretch()

        if len(self.decks)>0: self.on_deckChanged(self.decks[0])
        if len(self.models)>0: self.on_modelChanged(self.models[0])

        self.cursor = self.window.plugin.view.cursor
        self.cursor.selectedAreaByCursor.connect(
            self.on_cursor_selectedAreaByCursor)

        self.window.setTabLocation(self, self.location, self.name)

    def on_cursor_selectedAreaByCursor(self, event, pageItem, client):
        if client!=self: return

        text=self.cursor.getSelectionText()
        if text is None or len(text)==0: return
        text=' '.join(text)
        self.window.plugin.selector.copyToClipboard(text)

        if len(self.m_fields)==0: return 

        pageItem.setActions(self.m_fields)
        action = pageItem.m_menu.exec_(event.screenPos())

        if action.text() in self.m_fields:

            index=self.m_fields.index(action.text())
            for i in range(self.m_fieldLayout.count()):
                i=self.m_fieldLayout.itemAt(i)
                if i is None: continue
                w=i.widget()
                if w.m_row==index:
                    w.editor.setPlainText(text)
                    w.editor.show()

    def setAnkiData(self):
        collection=self.collection()
        self.decks= collection.decks.all_names()
        self.models = collection.models.all_names()
        collection.close()

    def on_savePressed(self):

        collection=self.collection()

        deck=self.deckWidget.currentText()
        model=self.modelWidget.currentText()

        deckId=collection.decks.by_name(deck)['id']
        model=collection.models.by_name(model)

        collection.decks.set_current(deckId)
        collection.models.set_current(model)

        note = collection.newNote()

        for i in reversed(range(self.m_fieldLayout.count())):
            i=self.m_fieldLayout.itemAt(i)
            if i is None: continue
            w=i.widget()
            text = w.editor.toPlainText()
            note.fields[w.m_row] = text
            if not w.button.isChecked():
                w.editor.clear()

        if self.window.view() is not None:

            did = self.window.view().document().id()
            page = self.window.view().currentPage()
            left, top=self.window.view().saveLeftAndTop()
            position=f'{left}:{top}'

        noteId=note.id

        self.window.plugin.tables.write(
                'anki', {'nid':noteId, 'did':did, 'page':page, 'position':position})

        collection.add_note(note, deckId)
        collection.save()

    def on_deckChanged(self, text):
        if text in self.decks:
            self.m_deck=text

    def on_modelChanged(self, text):
        if not text in self.models: return
        self.m_model=text
        self.m_fields=[]

        for i in reversed(range(self.m_fieldLayout.count())):
            i=self.m_fieldLayout.takeAt(i)
            if i is not None: i.widget().hide()

        collection=self.collection()
        for i, f in enumerate(collection.models.by_name(self.m_model)['flds']):
            field=f['name']
            self.m_fields+=[field]
            w=MQWidget(field, i)
            self.m_fieldLayout.addWidget(w)


    def toggle(self): 

        if not self.activated:

            self.activated=True
            self.window.plugin.view.cursor.activate(self, mode='selector')
            self.window.activateTabWidget(self)

        else:

            self.activated=False
            self.window.plugin.view.cursor.deactivate()
            self.window.deactivateTabWidget(self)

class MQWidget(QWidget):

    def __init__(self, title, row):
        super().__init__()
        self.m_title=title
        self.m_row=row
        self.setup()

    def setup(self):

        widget=QWidget(self)
        layout=QHBoxLayout(widget)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        self.title=QPushButton('+')
        self.title.setFixedWidth(20)
        self.title.pressed.connect(self.on_pressed)
        self.button=QRadioButton()
        self.button.setFixedWidth(20)
        self.button.setCheckable(True)

        layout.addWidget(QLabel(self.m_title))
        layout.addStretch()
        layout.addWidget(self.button)
        layout.addWidget(self.title)

        self.editor=QTextEdit()
        layout=QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(4)

        layout.addWidget(widget)
        layout.addWidget(self.editor)

        self.editor.hide()

    def on_pressed(self):
        if self.editor.isVisible():
            self.editor.hide()
            self.setFocus()
        else:
            self.editor.show()
            self.editor.setFocus()
