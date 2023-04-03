from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.plugins.documents import Documents
from lura.plugins.annotation import Annotation

class PluginManager(dict):
    def __init__(self, app):
        self.app=app
        self.config=app.config

    def activatePlugins(self):

        plugins=[
                    View,
                    Documents,
                    Annotation,
                    ]

        for plugin_class in plugins:
            config=self.get_config(plugin_class)
            plugin=plugin_class(self.app, config)
            setattr(self, plugin.name, plugin)
            self[plugin.name]=plugin

        self.set_plugin_shortcuts()

    def get_config(self, klass):
        name=klass.__name__
        return self.config['Plugins'].get(name, None)

    def set_plugin_shortcuts(self):
        for plugin in self.values():
            if hasattr(plugin, 'globalKeys'):
                for key, (func, parent, context) in plugin.globalKeys.items():
                    key=QKeySequence(key)
                    shortcut=QShortcut(key, parent)
                    shortcut.setContext(context)
                    shortcut.activated.connect(func)
