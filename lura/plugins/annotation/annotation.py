#!/usr/bin/python3

import re

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.utils import Plugin

class Annotation(Plugin):

    def __init__(self, app):
        super().__init__(app, name='annotation')

        self.selected=None
        self.set_config()

        self.app.window.keyPressEventOccurred.connect(self.on_keyPressEvent)
        self.app.window.mouseDoubleClickOccured.connect(self.on_mouseDoubleClickEvent)
        self.app.buffer.documentRegistered.connect(self.check_document)

    def on_mouseDoubleClickEvent(self, event, pageItem, view):
        pos=pageItem.mapToPage(event.pos())[1]
        for annotation in view.document().annotations(): 
            if annotation.page().pageItem()==pageItem:
                if annotation.contains(pos):
                    self.selected=annotation
                    return

    def on_keyPressEvent(self, event):
        if self.activated:
            if event.text() in self.colors:

                color_hex, desc=tuple(self.colors[event.text()].split(' '))
                color = QColor(color_hex)
                pageItem=self.app.window.view().pageItem()

                boundaries = []
                text, area=pageItem.getCursorSelection()
                for rectF in area: 
                    boundaries += [pageItem.mapToPage(rectF)[1]]

                if boundaries:
                    annotation = pageItem.page().annotate(
                            boundaries, color, 'highlightAnnotation')
                    self.register(annotation, boundaries)
                    pageItem.refresh(dropCachedPixmap=True)

            elif event.modifiers():  
                modifiers = QApplication.keyboardModifiers()
                if modifiers == Qt.ControlModifier:
                    if event.key()==Qt.Key_D and self.selected:
                        self.remove(self.selected)
                        self.selected=None

            self.activated=False

    def set_config(self):
        super().set_config()

        if self.config.has_section('Colors'):
            self.colors = dict(self.config.items('Colors'))

    def check_document(self, document):
        for ann in document.annotations():
            self.register(ann)

    def register(self, annotation, boundary=None):
        did = annotation.page().document().id()
        page = annotation.page().pageNumber()
        position=annotation.position()
        cond = {'did': did, 'page': page, 'position': position}
        aid=self.app.tables.get('annotations', cond, 'id') 
        if aid is None:
            data=cond.copy()
            content=[]
            size=annotation.page().size()
            t=QTransform().scale(size.width(), size.height())
            if type(boundary)!=list: boundary=[boundary]

            for b in boundary: 

                if b is None: continue

                x=.99*b.topLeft().x()
                topLeft=QPointF(x, b.topLeft().y())

                x=1.01*b.bottomRight().x()
                bottomRight=QPointF(x, b.bottomRight().y())

                b.setTopLeft(t.map(topLeft))
                b.setBottomRight(t.map(bottomRight))

                content+=[annotation.page().text(b)]

            if len(content)>0:
                data['content']=re.sub(re.compile(r'  *'), ' ', ' '.join(content))

            data['color']=annotation.color()

            self.app.tables.write('annotations', data)
            aid=self.app.tables.get('annotations', data, 'id')

        annotation.setId(aid)
        return annotation

    def remove(self, annotation):

        aid=self.app.tables.get('annotations',
                {'position':annotation.position(),
                    'page':annotation.page().pageNumber(),
                    'did': annotation.page().document().id()},
                'id')

        did=annotation.page().document().id()
        self.app.tables.remove('annotations', {'id': aid})
        annotation.page().removeAnnotation(annotation)
        annotation.page().pageItem().refresh(dropCachedPixmap=True)
