from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from plugin.utils import register
from plugin.widget import UpDownEdit

from lura.utils import Plugin, watch
from lura.utils import BaseInputListStack 

class Metadata(Plugin):

    excludeFields=['id', 'hash', 'url', 'kind']

    def __init__(self, app):

        super().__init__(app, name='metadata')

        self.setUI()

        self.app.window.display.viewChanged.connect(self.update)

    def setUI(self):

        self.ui=BaseInputListStack(self, 'right', item_widget=UpDownEdit)

        self.ui.main.input.hideLabel()
        self.ui.hideWanted.connect(self.deactivate)
        self.ui.main.list.widgetDataChanged.connect(self.on_contentChanged)

        self.ui.installEventFilter(self)

    def on_contentChanged(self, widget):

        value=widget.textDown()
        dhash=widget.data['hash']
        field=widget.data['field']
        self.app.tables.metadata.updateRow({'hash':dhash}, {field:value})

    def activate(self):

        self.activated=True
        self.ui.activate()

    def update(self):

        view=self.app.window.display.view
        if view and view.document():

            dhash=view.document().hash()
            meta=self.app.tables.metadata.getRow({'hash':dhash})
            dlist=[]
            if meta:
                for f, v in meta[0].items():
                    if f in self.excludeFields: continue
                    data={'up':f.title(), 'down':v, 'hash':dhash, 'field':f}
                    data['up_color']='green'
                    dlist+=[data]
            else:
                table_fields=self.app.tables.metadata.cleanFields()
                for f in table_fields:
                    if not f in self.excludeFields:
                        data={'up':f.title(), 'down':'', 'hash':dhash, 'field': f}
                        data['down_color']='green'
                        dlist+=[data]

            self.ui.main.setList(dlist)

    def deactivate(self):

        self.activated=False
        self.ui.deactivate()
