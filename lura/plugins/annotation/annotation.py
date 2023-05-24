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
        self.annotations={}
        self.set_config()

        self.app.window.mouseDoubleClickOccured.connect(self.on_mousePressEvent)
        self.app.window.mousePressEventOccured.connect(self.on_mousePressEvent)
        self.app.window.pageHasBeenJustPainted.connect(self.paint_annotations)
        self.app.buffer.documentRegistered.connect(self.check_document)

    def on_mousePressEvent(self, event, pageItem, view):
        pos=pageItem.mapToPage(event.pos())[1]
        for annotation in view.document().annotations(): 
            if annotation.page().pageItem()==pageItem:
                if annotation.contains(pos):
                    self.selected=annotation
                    return

    def deactivate(self):
        self.activated=False
        self.app.window.keyPressEventOccurred.disconnect(self.on_keyPressEvent)

    def activate(self):
        if not self.activated:
            self.activated=True
            self.app.window.keyPressEventOccurred.connect(self.on_keyPressEvent)
        else:
            self.deactivate()

    def on_keyPressEvent(self, event):
        if event.text() in self.colors:
            self.annotate(event.text())
        elif event.modifiers():  
            if QApplication.keyboardModifiers() == Qt.ControlModifier:
                if event.key()==Qt.Key_D and self.selected:
                    self.remove(self.selected)
                    self.selected=None
        self.deactivate()

    def set_config(self):
        super().set_config()

        if self.config.has_section('Colors'):
            self.colors = dict(self.config.items('Colors'))

    def check_document(self, document):
        did = document.id()
        if not did in self.annotations: self.annotations[did]={}
        annotations=self.app.tables.get('annotations', {'did':did}, unique=False)
        for annotation in annotations:
            page=int(annotation['page'])
            if not page in self.annotations[did]:
                self.annotations[did][page]=[]
            self.annotations[did][page]+=[annotation]

    def paint_annotations(self, painter, options, widgets, pageItem, view):
        did=pageItem.page().document().id()
        page=pageItem.page().pageNumber()
        if did in self.annotations:
            if page in self.annotations[did]:
                print(self.annotations[did][page])
                # raise #todo

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

    def annotate(self, text):
        color_hex, desc=tuple(self.colors[text].split(' '))
        color = QColor(color_hex)
        pageItem=self.app.window.view().pageItem()
        boundaries = []
        text, area=self.app.window.view().getCursorSelection()
        for rectF in area: 
            boundaries += [pageItem.mapToPage(rectF)[1]]
        if boundaries:
            annotation = pageItem.page().annotate(
                    boundaries, color, 'highlightAnnotation')
            self.register(annotation, boundaries)
            pageItem.refresh(dropCachedPixmap=True)
