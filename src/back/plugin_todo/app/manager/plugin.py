import os
import sys
import importlib

from ast import literal_eval

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Plugins(QObject):

    def __init__(self, app):

        super(Plugins, self).__init__(app)

        self.app=app
        self.plugins={}

    def load(self):

        if self.app.config.has_section('Manager'):
            self.manager_path=self.app.config.get('Manager', 'plugins_path') 
            sys.path.append(self.manager_path)
            if os.path.exists(self.manager_path):
                for p_name in os.listdir(self.manager_path):
                    if not p_name.startswith('__'):
                        plugin_module=importlib.import_module(p_name)
                        if hasattr(plugin_module, 'get_plugin_class'):
                            self.addPlugin(plugin_module.get_plugin_class())

        self.app.actionRegistered.emit()

    def loadPlugin(self, plugin_class):

        self.addPlugin(plugin_class)
        self.app.actionRegistered.emit()

    def addPlugin(self, plugin_class):

        plugin=plugin_class(self.app)
        self.plugins[plugin.name]=plugin
        setattr(self, plugin.name, plugin)
