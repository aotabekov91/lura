from plugin import WidgetPlug 
from lura.utils import BaseCommandStack 
from types import MethodType, BuiltinFunctionType

class Plugin(WidgetPlug):

    def __init__(self,

                 app, 
                 name=None, 
                 bar_data={},
                 mode_keys={}, 
                 position=None,
                 listening=False,
                 exclude_widget=[],
                 listen_leader=None,
                 listen_widget=None,
                 **kwargs):

        self.position=position
        self.bar_data=bar_data
        self.listening=listening
        self.mode_keys=mode_keys
        self.listen_widget=listen_widget
        self.exclude_widget=exclude_widget
        self.listen_leader=listen_leader

        if not 'argv' in kwargs: 
            kwargs['argv']=app.window

        super(Plugin, self).__init__(app=app, name=name, **kwargs)

        self.registerActions()

    def setUI(self): 

        self.ui=BaseCommandStack(self, self.position)
        self.ui.focusGained.connect(self.setFocus)

    def setFocus(self):

        self.app.modes.plug.setClient(self)
        self.app.modes.plug.activate()

    def modeKeys(self, mode): return self.mode_keys.get(mode, '')

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
                    self.commandKeys[method.key]=method

    def registerActions(self):

        self.setActions()
        self.app.manager.register(self, self.actions)
