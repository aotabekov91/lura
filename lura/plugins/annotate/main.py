import os
import functools

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin import InputList, ListWidget, UpDown

from lura.utils import Plugin, register
from lura.utils import getPosition, getBoundaries

class Annotation(Plugin):

    def __init__(self, app):

        super().__init__(app, position='right', mode_keys={'command': 'a'})

        self.app.window.buffer.documentCreated.connect(self.paint)
        self.app.window.display.viewChanged.connect(self.updateDisplay)

        # self.app.window.display.mousePressEventOccured.connect(self.on_mousePressEvent)

        self.setUI()

    def setActions(self):

        super().setActions()

        self.functions={}

        self.annotateActions={(self.__class__.__name__, 'toggle'): self.toggle}

        if self.config.has_section('Colors'):
            self.colors = dict(self.config.items('Colors'))
            self.colorList=[]
            for key, col in self.colors.items():

                color, function= tuple(col.split(' '))

                self.colorList+=[{'up': function, 'down':key, 'down_color':color}]

                self.functions[function]=color

                func=functools.partial(self.annotate, function=function)

                func.key=f'{key}'
                func.modes=['command', 'plug']

                self.commandKeys[key]=func
                self.actions[(self.__class__.__name__, function)]=func
                self.annotateActions[(self.__class__.__name__, function)]=func

                func=functools.partial(self.select, function=function)

                func.key=f'{key.title()}'
                func.modes=['command']

                self.commandKeys[key]=func
                self.actions[(self.__class__.__name__, function)]=func

        self.app.manager.register(self, self.actions)

    def setUI(self):

        super().setUI()

        colors=ListWidget(item_widget=UpDown)
        self.ui.addWidget(colors, 'colors')
        self.ui.colors.setList(self.colorList)

        display=InputList(item_widget=UpDown)
        display.input.hideLabel()

        self.ui.addWidget(display, 'display')
        self.ui.display.returnPressed.connect(self.open)
        self.ui.display.list.widgetDataChanged.connect(self.on_contentChanged)

        main=InputList(item_widget=UpDown, exact_match=True)
        main.input.hideLabel()

        self.ui.hideWanted.connect(self.deactivateUI)

        self.ui.installEventFilter(self)

    @register('o')
    def open(self):

        item=self.ui.display.list.currentItem()
        dhash=item.itemData['hash']
        page=item.itemData['page']
        boundaries=getBoundaries(item.itemData['position'])
        boundary=boundaries[0]
        topLeft=boundary.topLeft() 
        x, y = topLeft.x(), topLeft.y()

        view=self.app.window.display.currentView()
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

        item=self.ui.display.list.currentItem()
        nrow=self.ui.display.list.currentRow()-1

        if item:

            self.app.tables.annotation.removeRow({'id': item.itemData['id']})

            page=self.app.window.display.view.document().page(item.itemData['page'])
            page.removeAnnotation(item.itemData)
            page.pageItem().refresh(dropCachedPixmap=True)

            self.updateDisplay()
            self.ui.display.list.setCurrentRow(nrow)
            self.ui.display.setFocus()

    def select(self, function): raise

    def updateDisplay(self):

        view=self.app.window.display.currentView()
        annotations=view.document().annotations()

        for a in annotations:
            a['up']=f'# {a.get("id")}'
            a['down']=a['content']
            a['up_color']=a['color'].name()

        if annotations:
            self.ui.display.setList(annotations)
        else:
            self.ui.display.setList([])

    @register('s')
    def toggleDisplay(self):

        if self.activated:
            self.deactivateUI()
        else:
            self.activateDisplay()

    @register('a')
    def activateDisplay(self):

        self.activated=True

        self.app.modes.plug.setClient(self)
        self.app.modes.setMode('plug')

        self.ui.activate()
        self.ui.show(self.ui.display)

    @register('d')
    def deactivateUI(self):

        self.activated=False

        self.app.modes.plug.setClient()
        self.app.modes.setMode('normal')
        self.ui.deactivate()

    def annotate(self, function):

        selections=self.app.window.display.view.selection()

        if selections:

            selection=selections[0]

            text=selection['text']
            pageItem=selection['item']
            area=selection['area_unified']

            page=pageItem.page()
            pageNumber = page.pageNumber()
            dhash = page.document().hash()

            aData=self.write(dhash, pageNumber, text, area, function)
            self.add(page.document(), aData)

            pageItem.setSelection()
            pageItem.refresh(dropCachedPixmap=True)
            self.updateDisplay()

        self.deactivate()

    def write(self, dhash, pageNumber, text, boundaries, function):

        position=getPosition(boundaries)

        data = {'hash': dhash,
                'page': pageNumber,
                'position': position,
                'kind':'document',
                'text':text,
                'content':text,
                'function':function,
                }

        self.app.tables.annotation.writeRow(data)
        return self.app.tables.annotation.getRow(data)[0]

    def on_mousePressEvent(self, event, pageItem, view):

        # boundaries=[]
        # text, area=self.app.window.display.currentView().getCursorSelection(clear=True)
        # for rectF in area: boundaries += [pageItem.mapToPage(rectF)[1]]
        # print(text, area, boundaries, pageItem.m_boundingRect)

        self.selected=None
        pos=pageItem.mapToPage(event.pos())
        for annotation in view.document().annotations(): 
            if annotation.page().pageItem()==pageItem:
                if annotation.contains(pos):
                    self.selected=annotation
                    break
        # if self.selected: print('point', pos, self.selected.boundary())

    def paint(self, document):

        dhash = document.hash()
        aData=self.app.tables.annotation.getRow({'hash':dhash})
        for annotation in aData: self.add(document, annotation)

    def add(self, document, annotation):

        dhash = document.hash()
        page=document.page(annotation['page'])
        annotation['color'] = QColor(self.functions.get(annotation['function'], 'cyan'))
        annotation['boundaries']=getBoundaries(annotation['position'])
        annotation=page.annotate(annotation, kind='highlightAnnotation')

    @register('rs')
    def removeSelected(self):

        if self.selected:
            annotation=self.selected
            self.selected=None
            self.remove(annotation)
        self.setFocus()

    @register('a', modes=['normal','plug'])
    def toggle(self): 

        super().toggle()

        self.ui.activate()
        self.ui.show(self.ui.colors)

    def activate(self):

        self.activated=True
        self.listening=True

        self.app.manager.actions[self]=self.annotateActions

        self.app.modes.plug.delistenWanted.connect(self.deactivate)
        self.app.modes.plug.setClient(self)

        self.app.modes.setMode('plug')

    def deactivate(self):

        self.activated=False
        self.listening=False

        self.app.manager.actions[self]=self.actions

        self.app.modes.plug.delistenWanted.disconnect(self.deactivate)
        self.app.modes.plug.setClient()
        self.app.modes.setMode('normal')

        self.ui.deactivate()
