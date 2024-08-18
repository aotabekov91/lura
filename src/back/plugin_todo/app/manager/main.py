from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .mode import Modes
from .buffer import Buffer
from .plugin import Plugins

class Manager(QObject):

    bufferCreated=pyqtSignal(object)

    def __init__(self, app, buffer=None, mode=None, plugin=None):

        super(Manager, self).__init__(app)

        self.app=app
        self.actions={}

        self.setModeManager(mode)
        self.setBufferManager(buffer)
        self.setPluginManager(plugin)

    def register(self, plugin, actions): 

        self.actions[plugin]=actions
        self.app.actionRegistered.emit()

    def setModeManager(self, mode):

        if not mode: mode=Modes
        self.app.modes=mode(self.app)

    def setPluginManager(self, plugin):

        if not plugin: plugin=Plugins
        self.app.plugins=plugin(self.app)

    def setBufferManager(self, buffer): 

        if not buffer: buffer=Buffer
        self.app.buffer=buffer(self.app)
        self.app.buffer.bufferCreated.connect(self.bufferCreated)
