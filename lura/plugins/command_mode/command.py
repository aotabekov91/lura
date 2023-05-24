from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin import ListWidget
from lura.utils import Mode, BaseCommandStack

class Command(Mode):

    def __init__(self, app):

        super(Command, self).__init__(app=app)

        self.setUI()

        self.update()
        self.app.manager.pluginsLoaded.connect(self.update)

    def update(self): 
        
        dlist=[]

        for plugin, actions in self.app.manager.actions.items():

            for (plugin_name, func_name), method in actions.items():

                if method.command:

                    name=f'[{plugin_name}] {func_name}'
                    data={'id': method, 'up': name, 'plugin': plugin_name}
                    if method.key: 
                        data['down']=method.key

                    dlist+=[data]

        self.dlist=sorted(dlist, key=lambda x: x['plugin'])
        self.ui.main.setList(self.dlist, limit=None)

    def setUI(self):
        
        self.ui=BaseCommandStack(self, 'bottom')
        list_widget=ListWidget(check_fields=['down'], exact_match=True)
        self.ui.addWidget(list_widget, 'main', main=True)
        self.ui.hideWanted.connect(self.deactivate)
        self.ui.main.hideWanted.connect(self.deactivate)
        self.ui.main.returnPressed.connect(self.on_returnPressed)
        self.ui.installEventFilter(self)

    def on_returnPressed(self):

        self.deactivate()
        item=self.ui.main.item(self.ui.main.currentRow())
        partial=[]
        key, digit = self.checkKeys()

        if item and 'id' in item.itemData: partial=[item.itemData['id']]
        self.execute(partial, digit)

    def listen(self): 

        super().listen()
        self.ui.activate()
        self.statusbar('[Command]', kind='info')
        self.app.manager.listen(self.app, self)

    def delisten(self): 

        super().delisten()
        self.statusbar(kind='info')
        self.ui.main.unfilter()
        self.ui.deactivate()

    def findMatch(self, key, digit):

        self.ui.main.filter(key)
        partial=[]
        for i in range(self.ui.main.count()):
            partial+=[self.ui.main.item(i).itemData['id']]

        if len(partial)==0:
            self.ui.main.addItems([{'up': 'No match found'}])
        return partial

    def statusbar(self, text=None, kind='edit'):
        super().statusbar(text, kind)
        if not text: self.deactivate()
