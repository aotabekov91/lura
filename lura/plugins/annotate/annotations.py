import os
import functools

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin import InputList, ListWidget, UpDownEdit

from lura.utils import Plugin
from lura.utils import register, getPosition, getBoundaries

class Annotations(Plugin):

    def __init__(self, app, annotation):

        self.annotation=annotation

        super().__init__(app, position='right', mode_keys={'command': 'a'})

        self.app.main.buffer.documentCreated.connect(self.paint)
        self.app.main.display.viewChanged.connect(self.update)
        # self.app.main.display.mousePressEventOccured.connect(self.on_mousePressEvent)

        self.setUI()

    def setActions(self):

        super().setActions()

        self.functions={}

        self.annotateActions={(self.__class__.__name__, 'toggle'): self.toggle}

        if self.config.has_section('Colors'):
            self.colors = dict(self.config.items('Colors'))
            for key, col in self.colors.items():

                color, function= tuple(col.split(' '))

                func=functools.partial(self.select, function=function)
                func.key=f'{key.title()}'
                func.modes=[]

                self.commandKeys[key]=func
                self.functions[function]=color
                self.actions[(self.__class__.__name__, function)]=func

        self.app.manager.register(self, self.actions)

    def select(self, function): pass

    def setUI(self):

        super().setUI()

        self.ui.addWidget(InputList(item_widget=UpDownEdit), 'main', main=True)
        self.ui.main.input.hideLabel()
        self.ui.main.returnPressed.connect(self.open)
        self.ui.main.list.widgetDataChanged.connect(self.on_contentChanged)

        self.ui.hideWanted.connect(self.deactivate)
        self.ui.installEventFilter(self)

    @register('o')
    def open(self):

        item=self.ui.main.list.currentItem()
        aid=item.itemData['id']
        self.openById(aid)

    def openById(self, aid):

        data=self.app.tables.annotation.getRow({'id':aid})
        if data:
            data=data[0]
            dhash=data['hash']
            page=data['page']
            boundaries=getBoundaries(data['position'])
            boundary=boundaries[0]
            topLeft=boundary.topLeft() 
            x, y = topLeft.x(), topLeft.y()
            view=self.app.main.display.currentView()
            if view: view.jumpToPage(page, x, y-0.05)

    def on_contentChanged(self, widget):

        data=widget.data
        aid=data['id']
        text=widget.textDown()
        self.app.tables.annotation.updateRow({'id':aid}, {'content':text})

    @register('O')
    def openAndHide(self):

        self.open()
        self.deactivateUI()

    @register('D')
    def delete(self):

        item=self.ui.main.list.currentItem()
        nrow=self.ui.main.list.currentRow()-1

        if item:

            self.app.tables.annotation.removeRow({'id': item.itemData['id']})

            page=self.app.main.display.view.document().page(item.itemData['page'])
            page.removeAnnotation(item.itemData)
            page.pageItem().refresh(dropCachedPixmap=True)

            self.update()
            self.ui.main.list.setCurrentRow(nrow)
            self.ui.main.setFocus()

    def update(self):

        view=self.app.main.display.currentView()
        annotations=view.document().annotations()

        for a in annotations:
            a['up']=f'# {a.get("id")}'
            a['down']=a['content']
            a['up_color']=a['color'].name()

        if annotations:
            self.ui.main.setList(annotations)
        else:
            self.ui.main.setList([])

    @register('t', modes=['command'])
    def toggle(self):

        if self.activated:
            self.deactivate()
        else:
            self.activate()

    def activate(self):

        self.activated=True
        self.ui.activate()

    def deactivate(self):

        self.activated=False
        self.ui.deactivate()

    def paint(self, document):

        dhash = document.hash()
        aData=self.app.tables.annotation.getRow({'hash':dhash})
        for annotation in aData: 
            self.app.manager.annotation.add(document, annotation)
