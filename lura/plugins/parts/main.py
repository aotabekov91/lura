import os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from lura.utils import watch
from lura.utils import Plugin
from lura.utils.widgets import InputListLabel

from plugin.utils import register

from tables import DocumentParts

class Parts(Plugin):

    def __init__(self, app):
        super(Parts, self).__init__(app)

        self.parts=DocumentParts()
        self.setUI()

    def setUI(self):
        self.list=InputListLabel(self.app, self, 'right', 'Parts')
        self.list.returnPressed.connect(self.on_returnPressed)
        self.list.installEventFilter(self)

    def getHash(self):
        view=self.app.window.display.currentView()
        if view: return view.document().hash() 

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

    @watch('display', Qt.WidgetWithChildrenShortcut)
    def toggle(self):
        if not self.activated:
            self.activate()
        else:
            self.deactivate()
                
    def activate(self):
        self.activated=True
        self.setDataFor('abstract')
        self.list.activate()
        self.list.input.setFocus()

    @register('q')
    def deactivate(self):
        self.activated=False
        self.list.deactivate()

    @register('r')
    def showReference(self):
        self.setDataFor('reference')

    @register('a')
    def showAbstract(self):
        self.setDataFor('abstract')

    @register('o')
    def showOutline(self):
        self.setDataFor('section')

    @register('k')
    def showKeyword(self):
        self.setDataFor('keyword')

    @register('s')
    def showSummary(self):
        self.setDataFor('summary')

    @register('p')
    def showParagraph(self):
        dlist=self.setDataFor('paragraph')

    @register('b')
    def showBibliography(self):
        self.setDataFor('bibliography')

    def setDataFor(self, kind):
        dhash=self.getHash()
        if not dhash: return
        dlist=[]
        if kind=='reference':
            cites=[]
            if dhash:
                data=self.parts.cite.getRow({'citing_hash':dhash})
                if data:
                    for d in data:
                        cites+=self.parts.metadata.getRow({'bibkey':d['cited_bibkey']})
            else:
                cites=self.parts.metadata.getAll()
            for d in cites:
                b=f'{d["author"]}, {d["year"]}'
                dlist+=[{'up':d['title'], 'down':b, 'kind':'cite'}]
        else:
            table=getattr(self.parts, kind, None)
            if table:
                if dhash:
                    data=table.getRow({'hash':dhash})
                else:
                    data=table.getAll()
                for d in data:
                    doc_data=self.parts.metadata.getRow({'hash':d['hash']})
                    if doc_data:
                        name=doc_data[0]['title']
                    else:
                        name=d['hash']
                    dlist+=[{'up':d['text'], 'down':name, id:d['hash'], 'kind':kind}]
        self.list.setList(dlist)
        self.list.show()
        return dlist

    def on_returnPressed(self):
        page=0
        x, y = 0, 0
        view=self.app.window.display.currentView()
        if view:
            view.jumpToPage(page, x, y)
