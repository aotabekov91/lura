from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin.utils import register
from lura.utils import Plugin, watch
from lura.utils import BaseInputListStack

class Links(Plugin):

    def __init__(self, app):

        super().__init__(app)

        self.data={}
        self.links={}

        self.app.window.display.viewChanged.connect(self.on_viewChanged)
        self.app.window.display.mousePressEventOccured.connect(self.on_mousePressEventOccured)

        self.setUI()

    def setUI(self):

        self.ui=BaseInputListStack(self, 'bottom')

        self.ui.main.input.hideLabel()

        self.ui.hideWanted.connect(self.ui.deactivate)
        self.ui.main.returnPressed.connect(self.on_returnPressed)
        self.ui.main.list.currentItemChanged.connect(self.on_itemChanged)

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

    def deactivate(self):

        self.activated=False
        self.ui.deactivate()
        self.app.window.display.pageHasBeenJustPainted.disconnect(self.paintLinks)
        self.app.window.display.currentView().update()

    def activate(self):

        self.activated=True
        self.app.window.display.pageHasBeenJustPainted.connect(self.paintLinks)
        self.app.window.display.currentView().update()

    @watch('display')
    def toggleList(self):

        if not self.ui.isVisible():
            self.ui.activate()
        else:
            self.ui.deactivate()

    @watch('display')
    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()

    def on_mousePressEventOccured(self, event, pageItem, view):

        pos=pageItem.mapToPage(event.pos())[1]
        links=pageItem.m_page.links()
        for link in links:
            if link['boundary'].contains(pos):
                if link.get('page', None):
                    view.jumpToPage(link['page'])

    def paintLinks(self, painter, options, widget, pageItem, view):

        links=pageItem.m_page.links()

        painter.save()
        painter.setTransform(pageItem.m_normalizedTransform, True)
        painter.setPen(QPen(Qt.red, 0.0))

        for link in links: painter.drawRect(link['boundary'])

        painter.restore()
