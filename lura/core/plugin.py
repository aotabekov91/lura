from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.plugins.view import View
from lura.plugins.tables import Tables
from lura.plugins.documents import Documents
from lura.plugins.filebrowser import FileBrowser
from lura.plugins.tags import Tags
from lura.plugins.bookmarks import Bookmarks
from lura.plugins.annotation import Annotation
from lura.plugins.metadata import Metadata
from lura.plugins.links import Links
from lura.plugins.search import Search
from lura.plugins.notes import Notes
from lura.plugins.mindmap import MindMap
from lura.plugins.command import Command
from lura.plugins.outline import Outline
from lura.plugins.quickmarks import Quickmarks
from lura.plugins.selection import Selection
from lura.plugins.itemviewer import ItemView
from lura.plugins.pageinfo import PageInfo

# from lura.plugins.lookup import Lookup
# from lura.plugins.anki import Anki
# from lura.plugins.finder import Finder
# from lura.plugins.pomodoro import Pomodoro
# from lura.plugins.pager import Pager
# from lura.plugins.display import Display

from lura.plugins.buffers import Buffers
from lura.plugins.fuzzy import Fuzzy

class PluginManager(dict):
    def __init__(self, parent, s_settings):
        self.window=parent
        self.s_settings=s_settings

    def activatePlugins(self):

        plugins=[
                    View,
                    Fuzzy,
                    Tables,
                    Command,
                    Documents,
                    FileBrowser,
                    Metadata,
                    Links,
                    Annotation,
                    Bookmarks,
                    Notes,
                    MindMap,
                    Outline,
                    Quickmarks,
                    Search,
                    Tags,
                    Selection,
                    ItemView,
                    PageInfo,
                    # Anki,
                    # Lookup,
                    # Pager,
                    ]

        for Plugin in plugins:
            settings=self.getRelevantSettings(Plugin)
            plugin=Plugin(self.window, settings)
            setattr(self, plugin.name, plugin)
            self[plugin.name]=plugin

        self.setPluginShortcuts()

    def getRelevantSettings(self, klass):
        name=klass.__name__
        return self.s_settings['Plugins'].get(name, None)

    def setPluginShortcuts(self):
        for plugin in self.values():
            if hasattr(plugin, 'globalKeys'):
                for key, (func, parent, context) in plugin.globalKeys.items():
                    key=QKeySequence(key)
                    shortcut=QShortcut(key, parent)
                    shortcut.setContext(context)
                    shortcut.activated.connect(func)
