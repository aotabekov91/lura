#!/usr/bin/python3

from string import ascii_lowercase

from lura.utils import Plugin

class Links(Plugin):

    def __init__(self, app):
        super().__init__(app)
        self.links={}

        self.app.buffer.documentCreated.connect(self.on_documentCreated)
        self.app.window.mousePressEventOccured.connect(self.on_mousePressEventOccured)

    def on_documentCreated(self, document):
        if not document in self.links:
            self.links[document.hash()]=[]
            for page in document.pages():
                links=page.links()
                if links:
                    data=[page.pageNumber(), links]
                    self.links[document.hash()]+=[data]

    def deactivate(self):
        self.activated=False
        self.app.window.pageHasBeenJustPainted.disconnect(self.paintLinks)
        self.app.window.view().update()

    def activate(self):
        if not self.activated:
            self.activated=True
            self.app.window.pageHasBeenJustPainted.connect(self.paintLinks)
            self.app.window.view().update()
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

        for link in links:
            painter.drawRect(link['boundary'])

        painter.restore()
