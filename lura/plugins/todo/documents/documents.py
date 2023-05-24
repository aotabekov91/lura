from plugin.utils import register

from lura.utils import Plugin, watch
from lura.utils import InputListLabel

class Documents(Plugin):

    def __init__(self, app):
        super().__init__(app, name='documents')
        self.setUI()

    def setUI(self):
        self.ui=InputListLabel(self.app, self, 'right', 'Documents')
        self.ui.returnPressed.connect(self.on_returnPressed)
        self.ui.installEventFilter(self)

    @watch()
    def toggle(self):
        if not self.activated:
            self.activate()
        else:
            self.deactivate()

    def activate(self):
        self.activated=True
        self.ui.setList(self.getList())
        self.ui.activate()

    def getList(self):
        dlist=[]
        data=self.app.tables.hash.getAll()
        for d in data:
            d['up']=d['path'].split('/')[-1]
            meta=self.app.tables.metadata.getRow({'hash':d['hash']})
            if meta and meta[0]['title']:
                d['up']=meta[0]['title']
            if meta and meta[0]['author']: 
                d['down']=meta[0]['author']
            dlist+=[d]
        return dlist


    @register('q')
    def deactivate(self):
        self.activated=False
        self.ui.deactivate()

    def on_returnPressed(self):
        self.open()
        self.deactivate()

    @register('o')
    def open(self):
        item=self.ui.currentItem()
        if item:
            path=self.app.tables.hash.getPath(item.itemData['hash'])
            if path: 
                self.app.window.open(path)
        self.ui.input.setFocus()

