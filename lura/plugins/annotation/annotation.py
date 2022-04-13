#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .create import Creator
from .display import Display, AQWidget
from .connect import DatabaseConnector

class NQWidget(AQWidget):

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)

class Annotation(QObject):

    def __init__(self, parent, settings):
        super().__init__(parent)
        self.window=parent
        self.creator=Creator(self, settings)
        self.display=Display(self.window, settings)
        self.db=DatabaseConnector(self)
        self.s_settings=settings
        self.globalKeys={
                'Ctrl+h': (
                    self.creator.toggle,
                    self.window,
                    Qt.WindowShortcut),
                'Ctrl+Shift+s': (
                    self.display.toggle,
                    self.window,
                    Qt.WindowShortcut)
                }
        self.name = 'annotation'
        self.setup()

    def setup(self):

        self.window.documentRegistered.connect(self.db.checkDocument)
        self.window.annotationCreated.connect(self.db.register)

        self.window.mousePressEventOccured.connect(self.on_page_mousePressEvent)

    def on_page_mousePressEvent(self, event, pageItem, view):

        annotation=self.findAnnotation(event, pageItem, view)

        if annotation is None: return 

        if event.button()==Qt.LeftButton:
             self.activateProxyWidget(annotation, event, view)

        elif event.button()==Qt.RightButton:

            deleteAction=QAction('Delete')
            pageItem.setActions([deleteAction])
            action=pageItem.m_menu.exec_(event.screenPos())

            if action!=deleteAction: return 
            self.creator.remove(annotation)

    def activateProxyWidget(self, annotation, event, view):

        aid=self.window.plugin.tables.get('annotations',
                {'position':annotation.position(),
                    'page':annotation.page().pageNumber(),
                    'did': annotation.page().document().id()},
                'id')

        widget=NQWidget(aid, self.window)
        annotation.page().pageItem().addProxy(
                event.pos(), widget, widget.hide)

    def findAnnotation(self, event, pageItem, view):

        pos=pageItem.mapToPage(event.pos())[1]
        for annotation in view.document().annotations(): 
            if annotation.page().pageItem()!=pageItem: continue
            if annotation.boundary().contains(pos): return annotation

    def getAll(self, did):
        return self.db.getAll(did)

    def get(self, aid): 
        return self.db.get(aid)

    def getBy(self, condition):
        return self.db.getBy(condition)

    def registrator(self):
        return self.db

    def addAnnotation(self, *args, **kwargs):
        return self.creator.addAnnotation(*args, **kwargs)

    def colorSystem(self):
        return self.creator.system
