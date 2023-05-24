import os
import argparse
import functools

import threading

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin
from lura.utils import classify
from lura.utils.widgets import ListWidget

from .analyzer import pipeline

class Analysis(Plugin):

    def __init__(self, app):
        super().__init__(app)

        self.list=ListWidget(app, self, 'right', 'Analyzer')
        self.list.returnPressed.connect(self.on_returnPressed)

        self.app.window.buffer.documentCreated.connect(self.on_documentCreated)

    def on_documentCreated(self, document):

        return
        df=pipeline(document.filePath())
        print(df)


    def on_returnPressed(self):
        item=self.list.currentItem()

    @classify('list.input', Qt.WidgetWithChildrenShortcut)
    def remove(self):
        item=self.list.currentItem()
        nrow=self.list.currentRow()-1
        aid=item.itemData['id']
        self.app.manager.annotation.removeById(aid=aid)
        self.list.clear()

        criteria={'dhash':self.app.window.display.currentView().document().hash()}
        annotations = self.app.tables.get('annotations', criteria, unique=False)
        if annotations:
            for a in annotations:
                a['head']=f'# {a.get("id")}'
            self.list.setList(annotations)
            self.list.setCurrentRow(nrow)
        self.list.input.setFocus()

    @classify('display', Qt.WidgetWithChildrenShortcut)
    def toggle(self):
        if not self.activated:
            self.activated=True
            self.activateStatusbar()
            self.setData()
            self.list.activate()
            self.list.input.setFocus()
        else:
            self.deactivate()
                
    def setData(self, currentView=True):
        data=[]
        view=self.app.window.display.currentView()
        if currentView and view:
            data=self.analyzer.getParagraphs(view.document().filePath())
            data = self.app.tables.get('annotations', {}, unique=False)
            print(data)
        if data:
            print(data)
            data=list(data.values())
            for a in data:
                a['title']=f'# {a["keywords"]}'
                a['content']=a['text']
        self.list.setList(data)

    def deactivate(self):
        if self.activated:
            self.activated=False
            self.deactivateStatusbar()
            self.list.deactivate()
