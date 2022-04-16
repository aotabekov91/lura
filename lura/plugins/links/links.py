#!/usr/bin/python3

from string import ascii_lowercase

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.render.pdf import PdfDocument

class Links(QObject):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window=parent
        self.s_settings=settings
        self.globalKeys={
                'Ctrl+Shift+l': (
                    self.toggle,
                    self.window,
                    Qt.WindowShortcut),
                'g': (
                    self.goToWanted,
                    self.window,
                    Qt.WindowShortcut)
                }
        self.name='showLinks'
        self.setup()

    def goToWanted(self):
        view=self.window.view()
        if view is None or type(view.document())!=PdfDocument: return 
        self.window.plugin.command.activateCustom(
                self.goto, 'Go to: ')

    def goto(self, text):
        view=self.window.view()
        try:
            pageNumber=int(text)
        except:
            return
        view.jumpToPage(pageNumber)
        view.setFocus()

    def setup(self):

        self.links={}
        self.activated=False

        self.window.pageItemHasBeenJustCreated.connect(self.on_pageItemHasBeenJustCreated)
        self.window.mousePressEventOccured.connect(self.on_mousePressEventOccured)

    def toggle(self):

        if not self.activated:

            self.window.pageHasBeenJustPainted.connect(self.paintLinks)
            self.window.buffer.updateViews()
            self.activated=True

        else:

            self.window.pageHasBeenJustPainted.disconnect(self.paintLinks)
            self.window.buffer.updateViews()
            self.activated=False

    def on_pageItemHasBeenJustCreated(self, pageItem, view):
        document=view.m_document
        if not document in self.links:
            self.links[document]={}
        links=pageItem.m_page.links()
        if len(links)>0:
            self.links[document][pageItem]=links

    def on_mousePressEventOccured(self, event, pageItem, view):
        document=view.m_document
        pos=pageItem.mapToPage(event.pos())[1]
        if not pageItem in self.links[document]: return

        for link in self.links[document][pageItem]:
            if link['boundary'].contains(pos): break
            return 
        if link.get('page', None) is None: return 
        view.jumpToPage(link['page'])

    def paintLinks(self, painter, options, widget, pageItem, view):

        links=pageItem.m_page.links()

        if len(links)>0:

            painter.save()
            painter.setTransform(pageItem.m_normalizedTransform, True)
            painter.setPen(QPen(Qt.red, 0.0))

            for link in links:
                painter.drawRect(link['boundary'])

            painter.restore()
        

