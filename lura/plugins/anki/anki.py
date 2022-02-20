#!/usr/bin/python3

import shutil
import time

from collections import OrderedDict

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from anki.storage import Collection
from .table import AnkiNote

from bs4 import BeautifulSoup as BSHTML

class Anki(QScrollArea):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent
        self.s_settings=settings
        self.db=AnkiNote(self.window)
        self.name = 'Anki'
        self.globalKeys={
                'Ctrl+a': (
                    self.toggle, 
                    self.window,
                    Qt.WindowShortcut,
                    ), 
                }
        self.mediaFolder = '/home/adam/.local/share/Anki2/kim/collection.media/'

        # self.setup()

    def collection(self):
        return Collection('/home/adam/.local/share/Anki2/kim/collection.anki2')

    def activateImageSelector(self):
        self.selectionMode='image'
        self.cursor.activate(self, mode='rubberBand')

    def activateTextSelector(self):
        self.selectionMode='text'
        self.cursor.activate(self, mode='text'),

    def actOnCursorSelection(self, event, pageItem, client):

        if client==self:

            self.menu.clear()

            for (_, __, qaction) in self.currentWidget.fields.values():
                self.menu.addAction(qaction)

            if self.selectionMode=='text':

                text=' '.join(self.cursor.getSelectionText())

                self.selectionMode=None
                self.cursor.deactivate()

                action=self.menu.exec_(event.screenPos())

                for (qedit, qradio_, qaction) in self.currentWidget.fields.values():
                    if action==qaction:
                        qedit.insertPlainText(f' {text}')

            elif self.selectionMode=='image':

                rect=self.cursor.getRubberBandSelection()

                self.selectionMode=None
                self.cursor.deactivate()

                image=pageItem.m_page.render(
                        hResol=pageItem.scaledResolutionX(),
                        vResol=pageItem.scaledResolutionY(),
                        boundingRect=rect)
                
                imageFile='/tmp/{}.jpg'.format(int(time.time()))
                image.save(imageFile)

                action=self.menu.exec_(event.screenPos())

                for (qedit, qradio_, qaction) in self.currentWidget.fields.values():

                    if action==qaction:
                        cursor=qedit.textCursor()
                        cursor.insertImage(imageFile)
            self.setFocus()

    def setup(self):

        self.fuzzy=self.window.plugin.fuzzy
        self.fuzzy.fuzzySelected.connect(self.actOnFuzzySelection)

        self.activated=False
        self.selectionMode =None 

        self.shortcuts={v : k for k, v in self.s_settings['shortcuts'].items()}

        self.decks= self.collection().decks.all_names()
        self.models = self.collection().models.all_names()
        self.deck=self.decks[0]
        self.model=self.models[0]
        self.deckLabel=QLabel(self)
        self.modelLabel=QLabel(self)
        self.setAnkiData()

        self.ankiEdit=QLineEdit()
        self.ankiLabel=QLabel('Add new anki deck')
        self.ankiStatusBarWidget=QWidget()
        layout=QHBoxLayout(self.ankiStatusBarWidget)
        layout.addWidget(self.ankiLabel)
        layout.addWidget(self.ankiEdit)

        self.ankiEdit.returnPressed.connect(self.on_ankStatusBar)

        self.widgets={}
        self.currentWidget=None

        self.scrollArea=QScrollArea()
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.deckLabel)
        self.layout.addWidget(self.modelLabel)
        self.layout.addWidget(self.scrollArea)

        self.cursor=self.window.plugin.view.cursor
        self.cursor.selectedAreaByCursor.connect(self.actOnCursorSelection)

        self.menu=QMenu(self.window)

        self.window.setTabLocation(self, 'left', 'Anki')

    def keyPressEvent(self, event):
        key=event.text()

        if key in self.shortcuts:
            func=getattr(self, self.shortcuts[key])
            func()
            event.accept()
        else:
            if self.window.view() is None: return
            self.window.view().keyPressEvent(event)

    def changeModel(self):
        self.model=None
        self.fuzzy.setData(self, self.models)
        self.fuzzy.activate(self)

    def changeDeck(self):
        self.deck=None
        self.fuzzy.setData(self, self.decks)
        self.fuzzy.activate(self)

    def setAnkiData(self):

        deck=self.collection().decks.by_name(self.deck)
        model=self.collection().models.by_name(self.model)
        self.deckId=deck['id']
        self.collection().decks.set_current(self.deckId)
        self.collection().models.set_current(model)

        self.deckLabel.setText(f'Deck: {self.deck}')
        self.modelLabel.setText(f'Model: {self.model}')

    def actOnFuzzySelection(self, selected, listener):
        if self==listener:
            self.fuzzy.deactivate(self)
            # self.fuzzy.removeClient(self)
            if self.deck is None:
                self.deck=selected
            if self.model is None:
                self.model=selected
            
            self.setAnkiData()
            self.showModelWidget(self.model)
            self.activated=not self.activated
            self.toggle()

    def showModelWidget(self, model):

        self.scrollArea.takeWidget()

        if model not in self.widgets:

            widget=QWidget()
            self.widgets[model]=widget
            fields= self.getFields(self.model) 
            layout=QVBoxLayout(widget)

            widget.fields=OrderedDict()

            for i, field in enumerate(fields):

                qedit = CustomQEdit(self)
                # qedit.textChanged.connect(self.adjustTextEditorSize)
                # qedit.setFixedHeight(200)
                # qedit.setFixedWidth(200)
                qradio = QRadioButton(field)
                qaction=QAction(field)
                widget.fields[field]=(qedit, qradio, qaction)

                layout.addWidget(qradio)
                layout.addWidget(qedit)

            layout.addStretch()

            self.currentWidget=widget
            self.scrollArea.setWidget(self.currentWidget)
            self.scrollArea.setWidgetResizable(True)

        else:

            for m_model, widget in self.widgets.items():
                if m_model==model: 
                    self.currentWidget=widget
                    self.scrollArea.setWidget(self.currentWidget)

    def adjustTextEditorSize(self):
        widget=self.widgets[self.model]
        for field, (qedit, qradio, qaction) in widget.fields.items():
            size = qedit.document().size().toSize()
            if size.height() < 250:
                qedit.setFixedHeight(size.height()+15)


    def toggle(self, forceShow=False): 

        if not self.activated or forceShow:

            self.showModelWidget(self.model)
            self.window.activateTabWidget(self)
            self.setFocus()
            self.activated=True

        else:

            self.window.deactivateTabWidget(self)
            self.activated=False

    def getFields(self, model):
        fields=[]
        for f in self.collection().models.by_name(model)['flds']:
            fields+=[f['name']]
        return fields

    def addToField(self, fieldNumber):
        if self.kind == 'image':
            self.addImageToField(fieldNumber)
        elif self.kind == 'text':
            self.addTextToField(fieldNumber)

    def addTextToField(self, fieldNumber=None):
        if fieldNumber:
            field = self.fieldKeys[fieldNumber][0]
            rectangle = getattr(self.app.plugin.docViewer,
                                'rubberSelection', None)
            if rectangle != None:
                text = self.app.buffer.currentDocument.findText(
                    rectangle=rectangle)
                field.setText(text)
                self.app.plugin.docViewer.rubberSelection = None
                self.toggleAnkiMenu()
            else:
                self.parent.setFocus()
                self.toggle(mode='show')
                field.setFocus()

    def addImageToField(self, fieldNumber=None):
        if fieldNumber:
            field = self.fieldKeys[fieldNumber][0]
            rectangle = getattr(self.app.plugin.docViewer,
                                'rubberSelection', None)
            if rectangle != None:
                img = self.app.buffer.currentDocument.cutImage(
                    rectangle=rectangle)
                tmpLocation = '/tmp/{}.jpg'.format(int(time.time()))
                img.save(tmpLocation)
                document = field.document()
                cursor = field.textCursor()
                position = cursor.position()
                cursor.insertImage(tmpLocation)
                self.app.plugin.docViewer.rubberSelection = None
                self.toggleAnkiMenu()
            else:
                self.parent.setFocus()
                self.toggle(mode='show')
                field.setFocus()

    def addNewDeck(self):
        self.window.activateStatusBar(self.ankiStatusBarWidget)
        self.ankiEdit.setFocus()

    def on_ankStatusBar(self):
        deckName=self.ankiEdit.text()
        collection=self.collection()
        collection.decks.add_normal_deck_with_name(deckName)
        collection.save()
        self.window.deactivateStatusBar(self.ankiStatusBarWidget)
        self.deck=deckName
        self.setAnkiData()

    def submit(self):

        note = self.collection().newNote()

        self.setAnkiData()
        for i, field in enumerate(self.currentWidget.fields):
            qedit, qradio, qaction=self.currentWidget.fields[field]
            html = qedit.toHtml()
            for img in BSHTML(html).findAll('img'):
                src = img['src']
                newSrc = src.rsplit('/', 1)[-1]
                html = html.replace(src, newSrc)
                shutil.copyfile(src, self.mediaFolder+newSrc)
            note.fields[i] = html
            if not qradio.isChecked():
                qedit.clear()

        did = self.window.view.m_document.m_id
        page = self.window.view.m_currentPage
        left, top=self.window.view.saveLeftAndTop()
        position=f'{left}:{top}'
        noteId=note['id']

        self.db.write(noteId, did, page, position)

        note.add_tag(f'did:{did} page:{page} position:{position}')
        collection=self.collection()
        collection().add_note(note, self.deckId)
        collection.save()

    def clearFields(self):
        for (qedit, qradio, qaction) in self.currentWidget.fields.values():
            qedit.clear()

    def getNotes(self):
        # TODO
        did = self.app.buffer.currentDocument.id
        condition = 'tag:did:{}'.format(did)
        noteIds = self.collection().find_notes(condition)
        self.notes = [self.collection().get_note(n) for n in noteIds]
        fontHtmls = [n.items()[0][1] for n in self.notes]
        self.fuzzyItems = []
        for i, f in enumerate(fontHtmls):
            self.fuzzyItems += ['{}'.format(BSHTML(f).text).strip('\n')]
        self.fuzzy.setItems(self.fuzzyItems)
        self.fuzzy.toggle()

class CustomQEdit(QTextEdit):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent=parent

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.parent.setFocus()
        else:
            super().keyPressEvent(event)




