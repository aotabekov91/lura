from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin import InputList
from lura.utils import Plugin, register

class Links(Plugin):

    def __init__(self, app):

        super().__init__(app, position='bottom', mode_keys={'command': 'l'})

        self.data={}
        self.links={}

        self.app.window.display.viewChanged.connect(self.on_viewChanged)
        self.app.window.display.mousePressEventOccured.connect(self.on_mousePressEventOccured)

        self.setUI()

    def setUI(self):

        super().setUI()

        self.ui.addWidget(InputList(), 'main', main=True)
        self.ui.main.input.hideLabel()
        self.ui.main.returnPressed.connect(self.on_returnPressed)
        self.ui.main.list.currentItemChanged.connect(self.on_itemChanged)
        self.ui.hideWanted.connect(self.deactivate)
        self.ui.installEventFilter(self)

    def jump(self, match): pass

    def on_itemChanged(self, item):

        if item: self.jump(match=item.itemData)

    def on_returnPressed(self): self.deactivate()

    def on_viewChanged(self, view):

        document=view.document()
        if not document in self.links:
            self.data[document.hash()]=[]
            self.links[document.hash()]=[]
            for page in document.pages().values():
                links=page.links()
                if links:
                    data=[page.pageNumber(), links]
                    self.links[document.hash()]+=[data]
                    for link in links:
                        self.data[document.hash()]+=[self.updateLink(link)]

        self.ui.main.setList(self.data[document.hash()])

    def updateLink(self, link):

        if 'page' in link:
            link['up']=link['page']
            link['down']='goto'
        elif 'url' in link:
            link['up']=link['url']
            link['down']='link'
        return link

    @register('d')
    def deactivate(self):

        self.app.window.display.view.setPaintLinks(True)
        self.activated=False
        self.listening=False

        self.app.modes.plug.setClient()
        self.app.modes.setMode('normal')
        self.ui.deactivate()

        self.app.window.display.view.setPaintLinks(False)

    @register('a')
    def activate(self):

        self.activated=True
        self.listening=True

        self.app.modes.plug.setClient(self)
        self.app.modes.setMode('plug')

        self.app.window.display.view.setPaintLinks(True)

    @register('l')
    def toggleList(self):

        if not self.ui.isVisible():
            self.ui.activate()
        else:
            self.ui.deactivate()

    @register('t')
    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()

    def on_mousePressEventOccured(self, event, pageItem, view):

        pos=pageItem.mapToPage(event.pos())
        links=pageItem.m_page.links()
        for link in links:
            if link['boundary'].contains(pos):
                if link.get('page', None):
                    view.jumpToPage(link['page'])
