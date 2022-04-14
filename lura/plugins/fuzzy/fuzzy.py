from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import re

class Fuzzy(QWidget):

    fuzzySelected=pyqtSignal(object, object)

    def __init__(self, parent, settings):

        super().__init__(parent)
        self.window = parent
        self.s_settings=settings
        self.shortcuts={v:k for k, v in self.s_settings['shortcuts'].items()}
        self.location = 'top' 
        self.name = 'fuzzy'

        self.setup()

    def setup(self):

        self.activated = False
        self.client = None
        self.clients = {}

        self.window.setTabLocation(self, self.location, self.name)

        self.list = QListWidget(self)
        self.list.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.editor = QLineEdit(self)

        self.layout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.editor)
        self.layout.addWidget(self.list)

        self.editor.returnPressed.connect(self.act)
        self.editor.textChanged.connect(self.compare)

        self.editor.hide()

        shortcut = QShortcut(Qt.Key_Escape, self.editor)
        shortcut.activated.connect(self.showList)
        shortcut = QShortcut(Qt.Key_F, self.list)
        shortcut.activated.connect(self.showEditor)

    def showList(self):
        self.editor.hide()
        self.setFocus()

    def showEditor(self):
        self.editor.show()
        self.editor.setFocus()

    def clearCurrentData(self):

        self.client=None
        self.data=None
        self.items=None
        self.currentList=None

    def setData(self, client, data=None, names=None, indexChange=None):

        state = {
            'data': data,
            'names': names,
            'items': self.setItems(data, names),
        }

        if client in self.clients and  hasattr(self.clients[client], 'currentList'): 

            state['currentRow']=self.clients[client]['currentRow']+indexChange

            if indexChange==-1:

                for i, f in enumerate(self.clients[client]['currentList']):
                    f=' '.join(f.split(' ')[1:])
                    if not f in names:
                        self.clients[client]['currentList'].pop(i)
                state['currentList']=self.clients[client]['currentList']

            else:

                state['currentList']=self.clients[client]['currentList']

        else:

            state['currentRow']=0
            state['currentList']=self.setItems(data, names)

        self.clients[client] = state

    def saveState(self):

        if self.client is not None: 

            try:

                currentRow=self.currentList.index(self.list.currentItem().text())

                state = {
                    'data': self.data,
                    'names': self.names,
                    'items': self.items,
                    'currentList': self.currentList,
                    'currentRow': currentRow, 
                }

                self.clients[self.client] = state

            except AttributeError:
                pass

    def activateClient(self, client):

        # self.saveState()

        self.client=client

        if client in self.clients:

            self.data = self.clients[self.client]['data']
            self.items = self.clients[self.client]['items']
            self.names = self.clients[self.client]['names']
            self.currentList = self.clients[self.client]['currentList']
            self.currentRow=self.clients[self.client]['currentRow']

        else:

            raise

        self.cleanUp()

        self.addItems(self.currentList, self.currentRow)

    def cleanUp(self):
        self.list.clear()
        self.editor.clear()

    def setItems(self, data, names):

        if names is None:
            names = data

        items = []
        for i, name in enumerate(names):
            number = '{}'.ljust(len(str(len(names)))-len(str(i)))
            pos = number.format(i)
            items += ['{} {}'.format(pos, name)]
        return items

    def compare(self):
        text = self.editor.text()
        tmpList = []
        regex = '.*{}.*'.format('.*'.join([re.escape(t) for t in list(text)]))
        for item in self.items:
            if len(re.findall(regex, item.lower())) > 0:
                tmpList += [item]
        newList = []
        for i in range(len(text)+1):
            tmpText = text[:len(text)-i]
            regex = '.*{}.*'.format(tmpText)
            for j, item in enumerate(tmpList):
                if len(re.findall(regex, item)) > 0:
                    if not item in newList:
                        newList += [item]
                        tmpList.pop(j)
        newList += tmpList
        self.addItems(newList)

    def addItems(self, newList=None, currentRow=0):

        self.currentList = newList

        if self.currentList is None:

            self.currentList = self.items

        self.list.clear()

        for item in self.currentList:
            self.list.addItem(item)
        self.list.setCurrentRow(currentRow)

    def refresh(self, client):
        self.activateClient(client)
        self.list.show()
        self.setFocus()

    def activate(self, client):

        self.saveState()
        self.window.activateTabWidget(self)
        self.activateClient(client)
        self.list.show()
        self.setFocus()
        self.activated=True

    def deactivate(self, client):

        self.saveState()
        self.cleanUp()
        self.editor.hide()
        self.window.deactivateTabWidget(self)
        self.client=None
        self.data=None
        self.activated = False


    def toggle(self, client, forceShow=False):

        if self.client!=client:

            self.saveState()

            if not self.activated or forceShow:
                self.window.activateTabWidget(self)
                self.activated=True

            self.activateClient(client)
            self.list.show()
            self.setFocus()

        else:
            
            self.saveState()
            self.cleanUp()
            self.editor.hide()

            self.window.deactivateTabWidget(self)

            self.client=None
            self.data=None
            self.activated = False


    def getCurrentSelectedItem(self):

        try:
            selected = self.list.currentItem().text()
        except AttributeError:
            selected=self.list.item(self.currentRow)

        if selected is not None:
            return self.data[self.items.index(selected)]

    def removeClient(self, client):
        if client in self.clients:
            self.clients.pop(client)
            if self.client==client:
                self.client=None

    def act(self):
        self.fuzzySelected.emit(self.getCurrentSelectedItem(), self.client)
        self.deactivate(self.client)

    def moveDown(self):
        self._customMove(move='down')

    def moveUp(self):
        self._customMove(move='up')

    def _customMove(self, move='up'):
        index=self.currentList.index(self.list.currentItem().text())
        if move=='up':
            index-=1
        elif move=='down':
            index+=1
        if index>=len(self.currentList):
            index=0
        elif index<0:
            index=len(self.currentList)-1
        self.list.setCurrentRow(index)

    def onlyPreview(self):
        self.act()
        self.setFocus()

    def clearEditorFilter(self):
        self.clients[self.client]['currentList']=None
        client=self.client
        self.client=None
        self.toggle(client)

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            if hasattr(self.client, 'setFocus'):
                self.client.setFocus()
            self.deactivate(self.client)
        elif event.key() in [Qt.Key_Return, Qt.Key_L]:
            self.act()
        elif event.text() in self.shortcuts:
            key=event.text()
            func=getattr(self, self.shortcuts[key])
            func()
        else:
            try:
                self.client.keyPressEvent(event)
            except AttributeError:
                self.window.keyPressEvent(event)

