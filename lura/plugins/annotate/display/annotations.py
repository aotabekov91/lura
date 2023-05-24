import os
import functools

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import Plugin, watch
from lura.utils import getPosition, getBoundaries

from lura.utils import BaseInputListStack

class Annotations(Plugin):

    def __init__(self, app):

        super().__init__(app)

        self.setUI()
        self.app.window.display.viewChanged.connect(self.updateData)

    def setUI(self):

        self.ui=BaseInputListStack(self, 'right')

        self.ui.main.input.hideLabel()
        self.ui.hideWanted.connect(self.deactivate)
        self.ui.main.returnPressed.connect(self.on_returnPressed)
        self.ui.main.list.widgetDataChanged.connect(self.on_contentChanged)

        self.ui.installEventFilter(self)

    def setColors(self, colors):

        self.colors=colors
        self.functions={}
        actions={}
        for key, col in self.colors.items():
            color, function= tuple(col.split(' '))
            self.functions[function]=color
            func=functools.partial(self.updateData, function=function)
            func.key=f's{key}'
            actions[(func.key, function)]=func
            setattr(self, function, func)

        self.actions.update(actions)
        self.ui.commands.installEventFilter(self)
        self.app.manager.register(self, actions)

    def on_returnPressed(self):

        item=self.ui.main.list.currentItem()
        dhash=item.itemData['hash']
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
                    break
        self.ui.main.setFocus()

    def on_contentChanged(self, widget):

        data=widget.data
        aid=data['id']
        text=widget.textDown()
        self.app.tables.annotation.updateRow({'id':aid}, {'content':text})

    def open(self):

        self.on_returnPressed()
        self.app.window.display.setFocus()

    def remove(self):

        item=self.ui.main.list.currentItem()
        nrow=self.ui.main.list.currentRow()-1
        aid=item.itemData['id']
        self.app.manager.annotation.removeById(aid=aid)
        self.updateData()
        self.ui.main.list.setCurrentRow(nrow)
        self.ui.main.setFocus()

    @watch('window', Qt.WidgetWithChildrenShortcut)
    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()
                
    def updateData(self, currentView=True, function=None):

        annotations={}
        criteria={}

        if function: criteria['function']=function

        view=self.app.window.display.currentView()
        if currentView and view: criteria['hash']=view.document().hash()

        annotations = self.app.tables.annotation.getRow(criteria)

        if annotations:
            for a in annotations:
                a['up']=f'# {a.get("id")}'
                a['down']=a['content']
                a['up_color']=self.functions.get(a['function'], None)

        self.ui.main.setList(annotations)

    def activate(self):

        self.activated=True
        self.ui.activate()

    def deactivate(self):

        self.activated=False
        self.ui.deactivate()
