#!/usr/bin/python3

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .create import Creator
from .display import Display, AQWidget
from .connect import DatabaseConnector

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

        self.window.documentRegistered.connect(self.checkDocument)
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

            pageItem.refresh(dropCachedPixmap=True)


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
            if annotation.contains(pos): return annotation

    def checkDocument(self, document):
        for ann in document.annotations():
            self.db.register(ann)

class NQWidget(AQWidget):

    def on_titleChanged(self, text):
        super().on_titleChanged(text)
        self.m_window.plugin.annotation.display.update()

    def on_contentChanged(self):
        super().on_contentChanged(text)
        self.m_window.plugin.annotation.display.update()

    def keyPressEvent(self, event):
        if event.key()==Qt.Key_Escape:
            self.hide()
        else:
            super().keyPressEvent(event)
