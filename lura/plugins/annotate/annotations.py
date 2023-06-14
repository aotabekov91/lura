import os
import functools

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


from lura.utils import Plugin
from lura.utils import register, getPosition, getBoundaries

from plugin.widget import InputList, ListWidget, UpDownEdit

class Annotations(Plugin):

    def __init__(self, app, annotation):

        self.annotation=annotation

        super().__init__(app, position='right', mode_keys={'command': 'a'})

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
    def openAndFocus(self):

        self.open()
        self.app.modes.setMode('normal')

    @register('O')
    def open(self):

        item=self.ui.main.list.currentItem()
        if item:
            aid=item.itemData.get('id', None)
            if aid:
                self.openById(aid)
            else:
                self.openByData(item.itemData['pAnn'])

    def openByData(self, pAnn):

        boundary=pAnn.boundary()
        topLeft=boundary.topLeft() 
        x, y = topLeft.x(), topLeft.y()
        page=pAnn.page().pageNumber()
        view=self.app.main.display.currentView()
        if view: view.jumpToPage(page, x, y-0.05)

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

            self.app.tables.annotation.removeRow(
                    {'id': item.itemData.get('id', None)})

            page=self.app.main.display.view.document().page(
                item.itemData['page'])

            page.removeAnnotation(item.itemData)
            page.pageItem().refresh(dropCachedPixmap=True)

            self.update()
            self.ui.main.list.setCurrentRow(nrow)
            self.ui.main.setFocus()

    def update(self):

        view=self.app.main.display.currentView()
        annotations=view.document().annotations()
        native=view.document().nativeAnnotations()

        dhash=view.document().hash()

        for a in annotations:

            a['up']=f'# {a.get("id")}'
            a['down']=a['content']
            a['up_color']=a['color'].name()

        for n in native:
            data={
                  'pAnn':n,
                  'up': 'Native',
                  'hash': dhash,
                  'up_color':n.color(),
                  'down':n.contents(),
                  'kind': 'document',
                  'text': n.contents(),
                  'content': n.contents(),
                  'color': QColor(n.color()),
                  'page': n.page().pageNumber(),
                  }
            annotations+=[data]

        if annotations:
            self.ui.main.setList(annotations)
        else:
            self.ui.main.setList([])

    @register('t', modes=['command'])
    def toggle(self): super().toggle()

    def activate(self):

        self.update()
        self.app.main.display.viewChanged.connect(self.update)

        super().activate()

    def deactivate(self):

        self.app.main.display.viewChanged.disconnect(self.update)
        super().deactivate()
