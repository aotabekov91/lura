import os
import argparse
import functools

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin
from lura.utils import classify
from lura.utils.widgets import ListWidget
from lura.utils import getPosition, getBoundaries

class Annotations(Plugin):

    def __init__(self, app):
        self.list=ListWidget(app, self, 'right', 'Annotations')
        self.list.deleteWanted.connect(self.remove)
        self.list.contentUpdateOccurred.connect(self.on_contentChanged)
        self.list.returnPressed.connect(self.on_returnPressed)

        super().__init__(app)

        self.setParser()

    def filter(self, function):
        raise
        self.list.setText(f' -f {function} ')

    def setColors(self, colors):
        self.colors=colors
        self.functionToColor={}
        for key, c in self.colors.items():
            color, function=tuple(c.split(' '))
            self.functionToColor[function.lower()]=color

    def setParser(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-f', '--function')
        self.parser.add_argument('-i', '--id', type=int)
        self.parser.add_argument('content', nargs='?')

    def applyFilter(self, text, aData):
        try:
            parsed_args, unparsed_args = self.parser.parse_known_args(text.split())
        except:
            return False
        color=self.functionToColor.get(parsed_args.function, None)
        if color:
            if aData['color'].lower()!=color.lower(): return False
        if parsed_args.id:
            if aData['id']!=parsed_args.id: return False
        if parsed_args.content:
            if not parsed_args.content.lower() in aData['content'].lower(): return False
        return True

    def on_returnPressed(self):
        item=self.list.currentItem()
        dhash=item.itemData['dhash']
        page=item.itemData['page']
        boundaries=getBoundaries(item.itemData['position'])
        boundary=boundaries[0]
        topLeft=boundary.topLeft() 
        x, y = topLeft.x(), topLeft.y()
        data=self.app.tables.get('documents', {'hash': dhash}, unique=False)
        for f in data:
            if os.path.exists(f['path']):
                self.app.window.open(f['path'], how='reset')
                view=self.app.window.display.currentView()
                if view:
                    view.jumpToPage(page, x, y-0.4)
                    self.list.input.setFocus()
                    return

    def on_contentChanged(self, aid, text):
        self.app.tables.update('annotations', {'id':aid}, {'content':text})

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
        annotations={}
        view=self.app.window.display.currentView()
        if currentView and view:
            criteria={'dhash': view.document().hash()}
            annotations = self.app.tables.get('annotations', criteria, unique=False)
        else:
            annotations = self.app.tables.get('annotations', {}, unique=False)
        if annotations:
            for a in annotations:
                a['title']=f'# {a.get("id")}'
        self.list.setList(annotations)

    def deactivate(self):
        if self.activated:
            self.activated=False
            self.deactivateStatusbar()
            self.list.deactivate()
