#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class Creator(QObject):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window = parent.window
        self.m_parent = parent
        self.s_settings = settings
        self.setup()

    def createColorSystemActions(self):
        self.colorSystemActions = {}
        for key, color in self.system.items():
            self.colorSystemActions[QAction(key)] = color

    def setup(self):

        self.activated = False

        self.system = self.s_settings['colorSystem']
        self.createColorSystemActions()

        self.cursor = self.window.plugin.view.cursor
        self.cursor.selectedAreaByCursor.connect(
            self.on_cursor_selectedAreaByCursor)

    def toggle(self):

        if not self.activated:
            self.cursor.activate(self, mode='selector')
            self.activated = True

        else:

            self.activated = False
            self.cursor.deactivate()

    def act(self, event, unified, pageItem, listener):

        if listener != self:
            return

        pageItem.setActions(self.colorSystemActions)
        action = pageItem.m_menu.exec_(event.screenPos())

        if action in self.colorSystemActions:

            color = QColor(self.colorSystemActions[action])
            self.addAnnotation(unified, color, pageItem.page())

        pageItem.refresh(dropCachedPixmap=True)

    def on_cursor_selectedAreaByCursor(self, event, pageItem, client):

        if client != self:
            return

        boundaries = []
        for rectF in self.cursor.getSelectionArea():
            boundaries += [pageItem.mapToPage(rectF)[1]]

        if len(boundaries) == 0:
            return
        self.act(event, boundaries, pageItem, self)

    def addAnnotation(self, boundary, color, page):

        annotation = page.annotate(boundary, color, 'highlightAnnotation')
        self.m_parent.db.register(annotation)

        self.m_parent.display.update(page.document())

        return annotation

    def remove(self, annotation):

        aid=self.window.plugin.tables.get('annotations',
                {'position':annotation.position(),
                    'page':annotation.page().pageNumber(),
                    'did': annotation.page().document().id()},
                'id')
        self.window.plugin.tables.remove('annotations', {'id': aid})
        annotation.page().removeAnnotation(annotation)

        annotation.page().pageItem().refresh(dropCachedPixmap=True)
