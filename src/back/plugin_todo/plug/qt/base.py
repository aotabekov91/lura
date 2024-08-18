import os
import sys
import zmq
import time
import inspect

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ..plug import Plug
from ..utils import ZMQListener 

class PlugQT(Plug):

    def __init__(self, app,

                 name=None, 
                 config=None, 
                 port=None, 
                 argv=[],
                 command_leader=['.'],
                 command_activated=False,
                 ):

        super(PlugQT, self).__init__(name, config, port, argv)

        self.app=app
        self.command_leader=command_leader
        self.command_activated=command_activated

        self.actions={}
        self.commandKeys={}

        self.setSettings()
        self.setShortcuts()
        self.registerActions()

    def addLeader(self, leader):

        if not leader in self.command_leader:
            self.command_leader+=[leader]

    def setListener(self):

        self.listener = QThread()
        self.zeromq_listener=ZMQListener(self)
        self.zeromq_listener.moveToThread(self.listener)
        self.listener.started.connect(self.zeromq_listener.loop)
        self.zeromq_listener.request.connect(self.handle)
        QTimer.singleShot(0, self.listener.start)

    def setConnection(self, exit=True, kind=zmq.PULL):

        try:
            self.socket = zmq.Context().socket(kind)
            if self.port:
                self.socket.bind(f'tcp://*:{self.port}')
            else:
                self.port=self.socket.bind_to_random_port('tcp://*')
        except:
            if self.port:
                socket = zmq.Context().socket(zmq.PUSH)
                socket.connect(f'tcp://localhost:{self.port}')
                socket.send_json({'command':'show'})
                if exit:
                    sys.exit()
                else:
                    return socket

    def setShortcuts(self):

        if self.config.has_section('Shortcuts'):
            config=dict(self.config['Shortcuts'])
            for func_name, key in config.items():
                func=getattr(self, func_name, None)
                if func:
                    shortcut=QShortcut(key)
                    shortcut.activated.connect(func)
                    self.action[(key, func_name)]=func

    def registerActions(self):

        if hasattr(self, 'ui'):
            for name in self.ui.__dir__():
                method=getattr(self.ui, name)
                if hasattr(method, 'key'):
                    if not method.info: method.info=name
                    if not method.key or not method.key in self.commandKeys:
                        self.actions[(method.key, method.info)]=method

        for name in self.__dir__():
            method=getattr(self, name)
            if hasattr(method, 'key'):
                if not getattr(method, 'info', None): 
                    method.__func__.info=name
                    if not method.key or not method.key in self.commandKeys:
                        self.commandKeys[method.key]=method
                        # self.actions[(method.key, method.info)]=method.__func__
                        self.actions[(method.key, method.info)]=method 

        if self.config.has_section('Keys'):
            config=dict(self.config['Keys'])
            for name, key in config.items():
                method=getattr(self, name, None)
                if method:
                    setattr(method.__func__, 'key', key)
                    setattr(method.__func__, 'info', name)
                    if not method.key or not method.key in self.commandKeys:
                        self.commandKeys[method.key]=method
                        self.actions[(method.key, method.info)]=method 

    def eventFilter(self, widget, event):

        if event.type()==QEvent.KeyPress:

            if self.command_leader:
                if event.text() in self.command_leader and not self.command_activated:
                    self.leader_pressed=event.text()
                    self.activateCommandMode()
                    return True
                elif event.text() in self.command_leader and self.command_activated:
                    self.deactivateCommandMode()
                    return True

        return super().eventFilter(widget, event)

    def deactivateCommandMode(self):

        self.leader_pressed=None
        self.command_activated=False
        if hasattr(self, 'ui') and hasattr(self.ui, 'commands'):
            if self.ui.current==self.ui.commands: self.ui.show(self.ui.previous)

    def activateCommandMode(self):

        self.command_activated=True
        if hasattr(self, 'ui') and hasattr(self.ui, 'commands'):
            self.ui.show(self.ui.commands)
