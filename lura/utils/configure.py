import ast
from lura.utils import Plugin 

from types import MethodType, BuiltinFunctionType

class Configure(Plugin):

    def __init__(self, app, name, parent, **kwargs): 

        self.app=app
        self.name=name
        self.parent=parent
        self.setSettings()

        super().__init__(app, name, argv=None, **kwargs)

    def getSettings(self): return self.settings

    def setSettings(self):

        self.settings=None

        if self.app.config.has_section(f'{self.name}'):
            self.settings=self.app.config[f'{self.name}']

        # if self.app.config.has_section(f'{self.name}'):
        #     config=dict(self.app.config[f'{self.name}'])
        #     for name, value in config.items():
        #         try:
        #             value=ast.literal_eval(value)
        #         except:
        #             pass
        #         setattr(self, name, value)

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
