import os, sys
import importlib.util

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Manager(QObject):

    def __init__(self, app):

        super(Manager, self).__init__(app)

        self.app=app

        self.actions={}
        self.plugins={}
        self.speakers={}

    def loadPlugins(self):

        if self.app.config.has_section('Manager'):
            self.plugins_path=self.app.config.get('Manager', 'plugins_path') 
            sys.path.append(self.plugins_path)
            for p_name in os.listdir(self.plugins_path):
                if not p_name.startswith('__'):
                    plugin_module=importlib.import_module(p_name)
                    if hasattr(plugin_module, 'get_plugin_class'):
                        plugin_class=plugin_module.get_plugin_class()
                        plugin=plugin_class(self.app)
                        self.plugins[plugin.name]=plugin
                        setattr(self, plugin.name, plugin)

        self.app.actionRegistered.emit()

    def register(self, plugin, actions): 

        self.actions[plugin]=actions
        self.app.actionRegistered.emit()
