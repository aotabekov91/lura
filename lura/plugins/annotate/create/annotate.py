import functools

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin import UpDown
from plugin.utils import register as key

from lura.utils import getPosition, getBoundaries
from lura.utils import Plugin, watch, BaseInputListStack 

class Annotate(Plugin):

    def __init__(self, app):

        super().__init__(app) 

        self.selected=None
        self.annotations={}

        self.setUI()

        self.app.window.buffer.documentCreated.connect(self.paintDbAnnotations)
        self.app.window.display.mousePressEventOccured.connect(self.on_mousePressEvent)
        self.app.window.display.mouseDoubleClickOccured.connect(self.on_mousePressEvent)

    def setUI(self):

        self.ui=BaseInputListStack(self, 'bottom', item_widget=UpDown)

        self.ui.main.exact_match=True
        self.ui.main.input.hideLabel()

        self.ui.hideWanted.connect(self.deactivate)
        self.ui.main.returnPressed.connect(self.on_returnPressed)

        self.ui.installEventFilter(self)

    def on_returnPressed(self): 

        item=self.ui.main.list.currentItem()
        if item: item.itemData['id']()

    def activate(self):

        self.activated=True
        self.ui.activate()

    def deactivate(self):

        self.activated=False
        self.ui.deactivate()

    def on_mousePressEvent(self, event, pageItem, view):

        self.selected=None
        pos=pageItem.mapToPage(event.pos())[1]
        for annotation in view.document().annotations(): 
            if annotation.page().pageItem()==pageItem:
                if annotation.contains(pos):
                    self.selected=annotation
                    break
        if self.selected: print('point', pos, self.selected.boundary())

    def setColors(self, colors):

        self.colors=colors
        self.functions={}
        actions={}
        data=[]
        for key, col in self.colors.items():
            color, function= tuple(col.split(' '))
            self.functions[function]=color
            func=functools.partial(self.annotate, function)
            func.key=f'h{key}'
            actions[(func.key, function)]=func
            setattr(self, function, func)
            data+=[{'up':function, 'down':func.key, 'id':func, 'up_color':color}]
        self.actions.update(actions)
        self.ui.main.setList(data)
        self.app.manager.register(self, actions)

    def paintDbAnnotations(self, document):

        dhash = document.hash()
        annotations=self.app.tables.annotation.getRow({'hash':dhash})
        if annotations:
            for aData in annotations:
                page_number=aData['page']
                page=document.page(page_number)
                boundaries=getBoundaries(aData['position'])
                if page and boundaries: 
                    aData['boundaries']=boundaries
                    function=aData['function']
                    color = QColor(self.functions.get(function, 'black'))
                    annotation=page.annotate(boundaries, color, 'highlightAnnotation')
                    annotation.setId(aData['id'])

    def register(self, pageItem, text, boundaries, function, annotation):

        page=pageItem.page()
        dhash = page.document().hash()
        pageNumber = page.pageNumber()
        position=getPosition(boundaries)
        data = {'hash': dhash, 'page': pageNumber, 'position': position}
        aData=self.app.tables.annotation.getRow(data)
        if not aData:
            cond=data.copy()
            cond['kind']='document'
            cond['text']=' '.join(text)
            cond['content']=' '.join(text)
            cond['function']=function
            self.app.tables.annotation.writeRow(cond)
            aData=self.app.tables.annotation.getRow(data)
        aData=aData[0]
        aData['boundaries']=getBoundaries(aData['position'])
        annotation.setId(aData['id'])

    def removeById(self, aid):

        for annotation in self.app.window.display.currentView().document().annotations():
            if annotation.id()==aid:
                self.remove(annotation)
                self.setFocus()
                return
        self.app.tables.annotation.removeRow({'id': aid})
        self.setFocus()

    def removeSelected(self):

        if self.selected:
            annotation=self.selected
            self.selected=None
            self.remove(annotation)
        self.setFocus()

    def remove(self, annotation=None):

        if not annotation:
            return self.removeSelected()
        aid=annotation.id()
        annotation.page().removeAnnotation(annotation)
        if aid: self.app.tables.annotation.removeRow({'id': aid})
        self.app.window.display.currentView().pageItem().refresh(dropCachedPixmap=True)
        self.setFocus()

    def annotate(self, function):

        color = QColor(self.functions[function])
        pageItem=self.app.window.display.currentView().pageItem()
        boundaries = []
        text, area=self.app.window.display.currentView().getCursorSelection(clear=True)
        for rectF in area: boundaries += [pageItem.mapToPage(rectF)[1]]
        if boundaries:
            annotation = pageItem.page().annotate(boundaries, color, 'highlightAnnotation')
            self.register(pageItem, text, boundaries, function, annotation)
            pageItem.refresh(dropCachedPixmap=True)
        self.app.manager.annotation.updateData()
        self.deactivate()
