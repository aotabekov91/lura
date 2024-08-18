import os
import sys
import zmq
import ast
import time
import inspect

from os.path import abspath
from configparser import RawConfigParser

class Plug:

    def __init__(self, name=None, config=None, port=None, argv=None):

        if argv!=None:
            super(Plug, self).__init__(argv)
        else:
            super(Plug, self).__init__()

        self.name=name
        self.port=port
        self.config=config

        self.running = False
        self.activated=False

        self.setName()
        self.setConfig()
        self.setSettings()
        self.setConnection()

    def handle(self, request):

        print(f'{self.__class__.__name__} received: {request}')

    def readConfig(self): 

        file_path=os.path.abspath(inspect.getfile(self.__class__))
        folder_path=os.path.dirname(file_path).replace('\\', '/')
        config_path=f'{folder_path}/config.ini'
        config=RawConfigParser()
        config.optionxform=str
        config.read(config_path)
        return config

    def setName(self):

        if self.name is None: self.name=self.__class__.__name__.lower()

    def setConfig(self):

        if self.config is None: self.config=self.readConfig()

    def setSettings(self):

        if self.config.has_section('Settings'):
            config=dict(self.config['Settings'])
            for name, value in config.items():
                try:
                    value=ast.literal_eval(value)
                except:
                    pass
                attr=getattr(self, name, None)
                if not attr:
                    setattr(self, name, value)

    def setListener(self, kind=zmq.PULL):

        if self.port:
            self.socket = zmq.Context().socket(kind)
            self.socket.bind(f'tcp://*:{self.port}')

    def setConnection(self):

        if self.port:
            try:
                self.setListener()
            except:
                self.socket=None
                print(f'{self.port} is busy')

    def run(self):

        self.running=True
        while self.running and self.socket:
            request=self.socket.recv_json()
            answer=self.handle(request)
            if answer: self.socket.send_json(answer)

    def exit(self):

        self.running=False
