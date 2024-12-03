from types import MethodType, BuiltinFunctionType

from ...plug import PlugWidget 
from ...widget import BaseCommandStack 

class Plugin(PlugWidget):

    def __init__(self, app, name=None, mode_keys={}, position=None, **kwargs):

        self.position=position
        self.mode_keys=mode_keys

        if not 'argv' in kwargs: 
            kwargs['argv']=app.main

        super(Plugin, self).__init__(app=app, name=name, **kwargs)

        self.registerActions()

    def setUI(self): 

        self.ui=BaseCommandStack(self, self.position)

        self.ui.focusGained.connect(self.actOnFocus)
        self.ui.focusLost.connect(self.actOnDefocus)

    def actOnDefocus(self): 

        self.deactivateCommandMode()
        self.app.modes.setMode('normal')

    def actOnFocus(self):

        self.setStatusbarData()
        self.app.modes.setMode('me')

    def setStatusbarData(self):

        self.data={
                'detail': '',
                'client': self,
                'visible': True, 
                'info': self.name.title()
                }
        self.app.main.bar.setData(self.data)

    def modeKey(self, mode): return self.mode_keys.get(mode, '')

    def toggle(self):

        if not self.activated:
            self.activate()
        else:
            self.deactivate()

    def activate(self):

        self.activated=True
        if hasattr(self, 'ui'): self.ui.activate()

    def deactivate(self):

        self.activated=False
        if hasattr(self, 'ui'): self.ui.deactivate()


    def setShortcuts(self):

        if self.config.has_section('Shortcuts'):
            shortcuts=dict(self.config['Shortcuts'])
            for func_name, key in shortcuts.items():
                func=getattr(self, func_name, None)
                if func and hasattr(func, 'widget'): 
                    if func.widget=='window':
                        widget=self.app.main
                    elif func.widget=='display':
                        widget=self.app.main.display
                    else:
                        setattr(func, 'key', key)
                        continue
                    context=getattr(func, 'context', Qt.WidgetWithChildrenShortcut)
                    shortcut=QShortcut(widget)
                    shortcut.setKey(key)
                    shortcut.setContext(context)
                    shortcut.activated.connect(func)

    def setActions(self):

        # if hasattr(self, 'ui'):
        #     for name in self.ui.__dir__():
        #         method=getattr(self.ui, name)
        #         if hasattr(method, 'key'):
        #             if not method.info: method.info=name
        #             if not method.key or not method.key in self.commandKeys:
        #                 self.actions[(method.key, method.info)]=method

        if self.config.has_section('Keys'):
            config=dict(self.config['Keys'])
            for name, key in config.items():
                method=getattr(self, name, None)
                if method and hasattr(method, '__func__'):
                    setattr(method.__func__, 'key', f'{key}')
                    name=getattr(method, 'name', method.__func__.__name__)
                    modes=getattr(method, 'modes', ['command'])
                    setattr(method.__func__, 'name', name)
                    setattr(method.__func__, 'modes', modes)
                    data=(self.__class__.__name__, method.name)
                    self.actions[data]=method 
                    self.commandKeys[method.key]=method

        for name in self.__dir__():
            method=getattr(self, name)
            if type(method) in [MethodType, BuiltinFunctionType] and hasattr(method, 'modes'):
                data=(self.name, method.name)
                if not data in self.actions:
                    self.actions[data]=method 
                    if type(method.key)==str:
                        self.commandKeys[method.key]=method
                    elif type(method.key)==list:
                        for k in method.key: self.commandKeys[k]=method

    def registerActions(self):

        self.setActions()
        self.app.manager.register(self, self.actions)
