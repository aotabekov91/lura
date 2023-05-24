import os
import argparse
import functools

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin
from lura.utils.widgets.list import ListWidget
from lura.utils import getPosition, getBoundaries

class Annotations(Plugin):

    def __init__(self, app):
        self.list=ListWidget(app, self, 'bottom', 'annotations')
        self.list.deleteWanted.connect(self.remove)
        self.list.contentUpdateOccurred.connect(self.on_contentChanged)
        self.list.returnPressed.connect(self.on_returnPressed)

        super().__init__(app, name='annotations')

        self.setParser()
        self.setFunctionToColor()

    def set_shortcuts(self):
        super().set_shortcuts(parent_widget='window')

    def set_localcuts(self):
        super().set_localcuts(self.list.input)

    def filter(self, function):
        raise
        self.list.setText(f' -f {function} ')

    def set_config(self):
        super().set_config()
        if self.config.has_section('Colors'):
            self.colors = dict(self.config.items('Colors'))
        for key, col in self.colors.items():
            color, function= tuple(col.split(' '))
            func=functools.partial(self.filter, function)
            self.actions[function]=func
            context=Qt.WidgetWithChildrenShortcut
            shortcut=QShortcut(self)
            shortcut.setKey(key)
            shortcut.setContext(context)
            shortcut.activated.connect(func)
            shortcut.activatedAmbiguously.connect(func)

    def setFunctionToColor(self):
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
                self.app.window.open(f['path'], how='below')
                view=self.app.window.view()
                if view:
                    view.jumpToPage(page, x, y-0.4)
                    self.list.input.setFocus()
                    return

    def on_contentChanged(self, aid, text):
        self.app.tables.update('annotations', {'id':aid}, {'content':text})

    def remove(self):
        item=self.list.currentItem()
        nrow=self.list.currentRow()-1
        aid=item.itemData['id']
        self.app.plugin.annotation.removeById(aid=aid)
        self.list.clear()

        criteria={'dhash':self.app.window.view().document().hash()}
        annotations = self.app.tables.get('annotations', criteria, unique=False)
        if annotations:
            for a in annotations:
                a['head']=f'# {a.get("id")}'
            self.list.setList(annotations)
            self.list.setCurrentRow(nrow)
        self.list.input.setFocus()

    def activate(self):
        super().activate()
        if self.activated:
            self.list.clear()
            view=self.app.window.view()
            if view: 
                criteria={'dhash': self.app.window.view().document().hash()}
                annotations = self.app.tables.get('annotations', criteria, unique=False)
            else:
                annotations = self.app.tables.get('annotations', {}, unique=False)
            if annotations:
                for a in annotations:
                    a['head']=f'# {a.get("id")}'
                self.list.setList(annotations)
            self.list.activate()
            self.list.input.setFocus()
        else:
            self.deactivate()

    def deactivate(self):
        super().deactivate()
        if not self.activated:
            try:
                self.list.deactivate()
            except:
                # todo why try/except?
                pass
