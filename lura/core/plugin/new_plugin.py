from plugin.qt import Widget
from lura.utils import watch

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class NewPlugin(Widget):

    def __init__(self, app, name=None):
        super(NewPlugin, self).__init__(name=name, app=app.window)

        self.app=app
        self.activated=False
        self.setShortcuts()

    def activateStatusbar(self):
        statusbar=self.app.window.statusBar()
        statusbar.setDetailInfo(self.name)
        statusbar.show()

    def deactivateStatusbar(self):
        statusbar=self.app.window.statusBar()
        statusbar.setDetailInfo('')
        statusbar.hide()

    def activate(self, focus=True):
        if not self.activated:
            self.activated=True
            self.activateStatusbar()
            if focus:
                self.show()
                self.setFocus()

    def deactivate(self):
        if self.activated:
            self.activated=False
            self.deactivateStatusbar()
            self.app.window.display.focusCurrentView()

    @watch(widget='display', context=Qt.WidgetWithChildrenShortcut)
    def toggle(self):
        if not self.activated:
            self.activate()
        else:
            self.deactivate()

    def setShortcuts(self):
        if self.config.has_section('Shortcuts'):
            shortcuts=dict(self.config['Shortcuts'])
            for func_name, key in shortcuts.items():
                func=getattr(self, func_name, None)
                if func and hasattr(func, 'widget'): 
                    if func.widget=='window':
                        widget=self.app.window
                    elif func.widget=='display':
                        widget=self.app.window.display
                    else:
                        func.key=key
                        continue
                    context=getattr(func, 'context', Qt.WidgetWithChildrenShortcut)
                    shortcut=QShortcut(widget)
                    shortcut.setKey(key)
                    shortcut.setContext(context)
                    shortcut.activated.connect(func)
                    self.app.actions[f'{self.name}_{func_name}']=func
