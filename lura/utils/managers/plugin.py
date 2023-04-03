import os
import sys
import importlib.util

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class PluginManager(dict):

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def __init__(self, app):
        self.app=app
        self.plugins_path=self.app.config.get('Settings', 'plugins_path') 
        self.set_plugins()

    def set_plugins(self):

        sys.path.append(self.plugins_path)
        for p_name in os.listdir(self.plugins_path):
            if not p_name.startswith('__'):
                plugin_module=importlib.import_module(p_name)
                plugin_class=plugin_module.get_plugin_class()
                plugin=plugin_class(self.app)
                self[plugin.name]=plugin
