from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from plugin import ListWidget
from lura.utils import Mode, BaseCommandStack, register

class Command(Mode):

    def __init__(self, app):

        super(Command, self).__init__(app=app, 
                                      name='Command',
                                      show_commands=True, 
                                      key='c', 
                                      listen_leader=',')

        self.setUI()
        self.setData()

        self.app.manager.pluginsLoaded.connect(self.setData)

    def setData(self): 
        
        dlist=[]

        for plugin, actions in self.app.manager.actions.items():

            for (plugin_name, func_name), method in actions.items():

                if method.command:

                    method_name=getattr(method, 'info', None)
                    if method_name: func_name=method_name
                    name=f'[{plugin_name}] {func_name}'
                    data={'id': method, 'up': name, 'plugin': plugin_name}
                    if method.key: 
                        data['down']=method.key

                    dlist+=[data]

        self.dlist=sorted(dlist, key=lambda x: x['plugin'])
        self.ui.main.setList(self.dlist, limit=None)
