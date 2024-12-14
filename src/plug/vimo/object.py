import os
import inspect

class Object:

    name = None
    kind = None

    def __init__(
            self, 
            app=None, 
            config={},
            name=None, 
            parent=None, 
            manager=None,
            attributes=[],
            objectName=None,
            appConfig=False, 
            **kwargs,
            ):

        self.m_files = {}
        self.app = app
        self.m_name = name
        self.m_config = config
        self.m_parent = parent
        self.m_manager = manager
        self.m_app_config = appConfig
        self.m_objectName = objectName
        self.m_parent = parent
        self.m_attributes=attributes
        self.m_kwargs = kwargs
        super().__init__()
        self.setup()

    def setup(self):
        if self.m_app_config:
            self.setAppConfig()
        self.updateKlass()
        self.setAttributes()
        self.setConf()
        self.setName()
        self.setFiles()
        self.setKind()
        if self.m_manager:
            self.setManager(self.m_manager)
        if self.app:
            self.app.earman.add(self)

    def setAttributes(self):
        for attribute in self.m_attributes:
            print(attribute)
            #todo

    def getAttr(self, name, kind=None):
        return getattr(self, name, None)

    def updateKlass(self):
        pass

    def setManager(self, manager=None):
        if self.m_manager:
            self.m_manager.betChild(self)
        self.m_manager = manager
        if self.m_manager:
            self.m_manager.setChild(self)

    def manager(self):
        return self.m_manager

    def setName(self, name=None):
        if not name:
            c = self.__class__.__name__
            c = self.m_name or c
            name = self.name or c
        self.name = name

    def setConf(self, data=None):
        data = data or self.m_config
        if not data:
            return
        for k, v in data.items():
            setattr(self, k, v)

    def getConfig(self, config):
        conf = {}
        for i in self.__class__.__mro__[::-1]:
            n = i.__name__
            conf.update(config.get(n, {}))
        conf.update(config.get(self.name, {}))
        return conf

    def setAppConfig(self):
        if self.app:
            aconfig = self.app.m_config
            conf = self.getConfig(aconfig)
            self.m_config.update(conf)

    def config(self):
        return self.m_config

    def setProp(self, name, value=True, view=None):
        view = view or self
        setattr(view, name, value)

    def delProp(self, what):
        delattr(self, what)

    def getProp(self, what, view=None):
        view = view or self
        return getattr(view, what, None)

    def checkProp(self, what, view=None):
        view = view or self
        if type(what) != list:
            what = [what]
        for w in what:
            if not getattr(view, w, False):
                return False
        return True

    def __bool__(self):
        return True

    def setFiles(self):
        f = inspect.getfile(self.__class__)
        a = os.path.abspath(f)
        p = os.path.dirname(a)
        self.path = p.replace("\\", "/")
        for f in os.listdir(self.path):
            p = f"{self.path}/{f}"
            self.m_files[f] = p

    def setKind(self):
        name = self.__class__.__name__
        self.kind = self.kind or name

    def resetConfigure(self, **kwargs):
        pass
