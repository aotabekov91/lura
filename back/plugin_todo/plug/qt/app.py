import os
import sys
import inspect

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .base import PlugQT

class PlugApp(PlugQT, QApplication):

    def __init__(self, name=None, config=None, leader=None, port=None, app_name=None):

        super(PlugApp, self).__init__(name, config, leader, port) 
        self.app_name=app_name
        self.setAppName()

    def setAppName(self):

        if not self.app_name: self.app_name=self.name
        self.setApplicationName(self.app_name)

    def handle(self, request):

        command=request['command']

        func=getattr(self, command, None)
        if not func and hasattr(self, 'ui'): func=getattr(self.ui, command, None)

        if func:
            if 'request' in inspect.signature(func).parameters:
                func(request)
            else:
                func()
            msg=f"{self.__class__.__name__}: handled request"
        else:
            msg=f'{self.__class__.__name__}: not understood'

        print(msg)

    def run(self):

        self.running=True
        self.setListener()
        sys.exit(self.exec_())

    def exit(self): 

        self.running=False
        sys.exit()

if __name__=='__main__':
    app=PlugApp(port=33333)
    app.run()
