from ..base import Plugin 

from types import MethodType, BuiltinFunctionType

class Configure(Plugin):

    def __init__(self, app, name, parent, **kwargs): 

        self.app=app
        self.name=name
        self.parent=parent
        self.parent.modeKey=self.modeKey
        self.setSettings()

        super().__init__(app, name, argv=None, **kwargs)

    def getSettings(self): return self.settings

    def setSettings(self):

        self.settings=None

        if self.app.config.has_section(f'{self.name}'):
            self.settings=self.app.config[f'{self.name}']

    def setActions(self):

        for name in self.parent.__dir__():
            method=getattr(self.parent, name)
            if type(method) in [MethodType, BuiltinFunctionType] and hasattr(method, 'modes'):
                data=(self.name, method.name)
                if not data in self.actions:
                    self.actions[data]=method 
                    self.commandKeys[method.key]=method

    def registerActions(self):

        self.setActions()
        self.app.manager.register(self.parent, self.actions)
