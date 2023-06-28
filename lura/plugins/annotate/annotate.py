import functools

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin.app.mode import Mode
from plugin.widget import ListWidget, UpDown

from lura.utils import getPosition 

class Annotate(Mode):

    def __init__(self, app, annotation):

        self.annotation=annotation

        super().__init__(app,
                         listen_leader='a',
                         show_commands=True,
                         show_statusbar=True,
                         )

        self.setUI()

    def setActions(self):

        super().setActions()
        self.annotateActions={(self.__class__.__name__, 'toggle'): self.toggle}

        if self.config.has_section('Colors'):
            self.colors = dict(self.config.items('Colors'))
            self.colorList=[]
            for key, col in self.colors.items():

                color, function= tuple(col.split(' '))

                up=f'{key} - {function}'
                self.colorList+=[{'up': up, 'up_color':color}]

                self.annotation.functions[function]=color
                func=functools.partial(self.annotate, function=function)
                func.key=f'{key}'
                func.modes=[]
                self.commandKeys[key]=func
                self.actions[(self.__class__.__name__, function)]=func
                self.annotateActions[(self.__class__.__name__, function)]=func

        self.app.manager.register(self, self.actions)

    def setUI(self):

        super().setUI()

        self.ui.addWidget(ListWidget(item_widget=UpDown), 'mode', main=True)
        self.ui.main.setList(self.colorList)
        self.ui.mode.hideWanted.connect(self._onExecuteMatch)

    def _onExecuteMatch(self):

        self.ui.dock.hide()
        super()._onExecuteMatch()

    def listen(self):

        if self.app.main.display.view: super().listen()

    def annotate(self, function):

        self.deactivate()

        selections=self.app.main.display.view.selected()

        if selections:

            selection=selections[0]

            text=selection['text']
            pageItem=selection['item']
            area=selection['area_unified']

            page=pageItem.page()
            pageNumber = page.pageNumber()
            dhash = page.document().hash()

            aData=self.write(dhash, pageNumber, text, area, function)

            self.annotation.add(page.document(), aData)

            self.annotation.update()

            pageItem.select()
            pageItem.refresh(dropCachedPixmap=True)
            self.update()

    def write(self, dhash, pageNumber, text, boundaries, function):

        position=getPosition(boundaries)

        data = {'hash': dhash,
                'page': pageNumber,
                'position': position,
                'kind':'document',
                'content':text,
                'function':function,
                }

        self.app.tables.annotation.writeRow(data)

        for f in ['function', 'kind', 'content']: data.pop(f)
        return self.app.tables.annotation.getRow(data)[0]

    def activateCheck(self, event): 

        if super().activateCheck(event):

            view=self.app.main.display.view
            if view:
                v=self.app.modes.visual
                visual=v.listening and not v.hinting
                normal=self.app.modes.normal.listening
                return normal or visual
            else:
                return False
