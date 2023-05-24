#!/usr/bin/python3

import re
import functools

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.utils import Plugin
from lura.utils import getPosition, getBoundaries

class Annotator(Plugin):

    def __init__(self, app):
        super().__init__(app, name='annotation')

        self.selected=None
        self.annotations={}

        self.app.window.mouseDoubleClickOccured.connect(self.on_mousePressEvent)
        self.app.window.mousePressEventOccured.connect(self.on_mousePressEvent)
        self.app.buffer.documentRegistered.connect(self.paintDbAnnotations)

    def on_mousePressEvent(self, event, pageItem, view):
        self.selected=None
        pos=pageItem.mapToPage(event.pos())[1]
        for annotation in view.document().annotations(): 
            if annotation.page().pageItem()==pageItem:
                if annotation.contains(pos):
                    self.selected=annotation
                    break
        if self.selected:
            print('point', pos, self.selected.boundary())
        return

    def set_config(self):
        super().set_config()
        if self.config.has_section('Colors'):
            self.colors = dict(self.config.items('Colors'))
        for key, col in self.colors.items():
            color, function= tuple(col.split(' '))
            func=functools.partial(self.annotate, color)
            self.actions[function]=func
            context=Qt.WidgetWithChildrenShortcut
            shortcut=QShortcut(self)
            shortcut.setKey(key)
            shortcut.setContext(context)
            shortcut.activated.connect(func)
            shortcut.activatedAmbiguously.connect(func)

    def paintDbAnnotations(self, document):
        dhash = document.hash()
        annotations=self.app.tables.get('annotations', {'dhash':dhash}, unique=False)
        if annotations:
            for aData in annotations:
                page_number=aData['page']
                page=document.page(page_number)
                boundaries=getBoundaries(aData['position'])
                if page and boundaries: 
                    aData['boundaries']=boundaries
                    color = QColor(aData['color'])
                    annotation=page.annotate(boundaries, color, 'highlightAnnotation')
                    annotation.setId(aData['id'])

    def register(self, pageItem, text, boundaries, color, annotation):
        page=pageItem.page()
        dhash = page.document().hash()
        pageNumber = page.pageNumber()
        position=getPosition(boundaries)
        data = {'dhash': dhash, 'page': pageNumber, 'position': position}
        aData=self.app.tables.get('annotations', data)
        if aData is None:
            cond=data.copy()
            cond['title']=' '.join(text)
            cond['content']=' '.join(text)
            cond['color']=color
            self.app.tables.write('annotations', cond)
            aData=self.app.tables.get('annotations', data)
        aData['boundaries']=getBoundaries(aData['position'])
        annotation.setId(aData['id'])

    def removeById(self, aid):
        for annotation in self.app.window.view().document().annotations():
            print(annotation.id())
            if annotation.id()==aid:
                self.remove(annotation)
                self.setFocus()
                return
        self.app.tables.remove('annotations', {'id': aid})
        self.setFocus()

    def removeSelected(self):
        if self.selected:
            annotation=self.selected
            self.selected=None
            self.remove(annotation)
        self.setFocus()

    def remove(self, annotation=None):
        if not annotation:
            return self.removeSelected()
        aid=annotation.id()
        annotation.page().removeAnnotation(annotation)
        if aid: self.app.tables.remove('annotations', {'id': aid})
        self.app.window.view().pageItem().refresh(dropCachedPixmap=True)
        self.setFocus()

    def annotate(self, color_hex):
        color = QColor(color_hex)
        pageItem=self.app.window.view().pageItem()
        boundaries = []
        text, area=self.app.window.view().getCursorSelection(clear=True)
        for rectF in area: 
            boundaries += [pageItem.mapToPage(rectF)[1]]
        if boundaries:
            annotation = pageItem.page().annotate(
                    boundaries, color, 'highlightAnnotation')
            self.register(pageItem, text, boundaries, color_hex, annotation)
            pageItem.refresh(dropCachedPixmap=True)
        self.deactivate()
