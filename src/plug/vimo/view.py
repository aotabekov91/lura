import os
import inspect


class View:
    isView = True
    name = None
    kind = None
    position = {}
    prefix_keys = []
    activated = False
    default_mode = "normal"

    def __init__(
        self,
        app=None,
        config={},
        name=None,
        model=None,
        index=None,
        pindex=None,
        parent=None,
        manager=None,
        identifier=None,
        objectName=None,
        appConfig=False,
        **kwargs,
    ):
        self.app = app
        self.m_files = {}
        self.m_id = index
        self.m_name = name
        self.m_pid = pindex
        self.m_children = {}
        self.m_model = model
        self.m_kwargs = kwargs
        self.m_config = config
        self.m_parent = parent
        self.m_vid = identifier
        self.m_manager = manager
        self.m_app_config = appConfig
        self.m_objectName = objectName
        self.m_parent = parent
        super().__init__()
        self.setup()

    def setup(self):
        if self.m_app_config:
            self.setAppConfig()
        self.updateKlass()
        self.setConf()
        self.setName()
        self.setFiles()
        self.addToAppUI()
        if self.m_manager:
            self.setManager(self.m_manager)
        if self.app:
            self.app.earman.add(self)

    def addToAppUI(self):
        if not self.checkProp("app", self):
            return
        if not self.checkProp("buffman", self.app):
            return
        self.app.buffman.addView(self)

    def getAttr(self, name, kind=None):
        return getattr(self, name, None)

    def updateKlass(self):
        pos = self.m_kwargs.get("position")
        if pos:
            self.position.update(pos)
        prefixes = self.m_kwargs.get("prefix_keys")
        if prefixes:
            self.prefix_keys += prefixes

    def setIdentifier(self, idx):
        self.m_vid = idx

    def identifier(self):
        return self.m_vid

    def setManager(self, man=None):
        if self.m_manager:
            self.m_manager.betChild(self)
        self.m_manager = man
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

    def child(self, pos, recursive=True):
        if pos.startswith("!"):
            child = self.m_children.get(pos[1:])
            if child:
                return child
            elif recursive:
                for i in self.m_children.values():
                    child = i.child(pos, recursive)
                    if child:
                        return child
        elif pos:
            p = pos.split("|", 1)
            child = self.m_children.get(p[0])
            if not child:
                return self
            elif len(p) == 1:
                return child
            elif not child is None and recursive:
                return child.child(p[1], recursive)

    def setChild(self, obj):
        pidx = obj.posIndex()
        idx = obj.identifier()
        if not idx is None:
            self.m_children[str(idx)] = obj
        if not pidx is None:
            self.m_children[str(pidx)] = obj

    def betChild(self, obj):
        c = None
        pidx = obj.posIndex()
        idx = obj.identifier()
        if not idx is None:
            c = self.m_children.pop(str(idx), None)
        if not pidx is None:
            c = self.m_children.pop(str(pidx), None)
        return c

    def updateChildIndex(self, n, o, child):
        self.m_children.pop(o, None)
        self.m_children[n] = child

    def setIndex(self, index=None):
        self.m_id = index

    def index(self):
        return self.m_id

    def posIndex(self):
        return self.m_pid

    def fullPosIndex(
        self,
        suffix="",
        recursive=True,
    ):
        pidx = self.posIndex()
        idx = self.identifier()
        c1 = not idx is None
        c2 = not pidx is None
        sep = self.m_kwargs.get("suffix_separator", "|")
        sep = getattr(self, "suffix_separator", sep)
        if c1 and c2:
            fidx = f"{pidx}[{idx}]"
        elif idx:
            fidx = str(idx)
        else:
            fidx = str(pidx)
        if suffix:
            suffix = f"{fidx}{sep}{suffix}"
        else:
            suffix = fidx
        if recursive:
            m = self.m_manager
            if m and m != self.app.ui:
                return m.fullPosIndex(suffix, recursive)
        return suffix

    def setPosIndex(self, idx=None):
        self.m_pid = idx

    def model(self):
        return self.m_model

    def setModel(self, model):
        if id(self.m_model) != id(model):
            self.m_model = model
            self.kind = model.kind

    def setProp(self, name, value=True, view=None):
        view = view or self
        setattr(view, name, value)

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

    @classmethod
    def isCompatible(cls, m, **kwargs):
        n = cls.name or cls.__name__
        return n in getattr(m, "wantView", [])

    def toggle(self, *args, **kwargs):
        if self.activated and self.isVisible():
            self.octivate(*args, **kwargs)
        else:
            self.activate(*args, **kwargs)

    def octivate(self, *args, **kwargs):
        m = self.manager()
        self.activated = False
        if self.app:
            self.app.stateman.betView(self)
        if m:
            m.betView(self, *args, **kwargs)

    def activate(
            self, 
            *args, 
            recursive=False,
            **kwargs
            ):
        self.activated = True
        manager = self.manager()
        if manager:
            manager.setView(*args, view=self, **kwargs)
            if recursive and not manager.activated:
                manager.activate(recursive=recursive)
        self.app.stateman.setView(view=self)
        if self.checkProp("setFocus"):
            self.show()
            self.setFocus()

    def betView(
        self,
        view,
        recursive_octivate=False,
        **kwargs,
    ):
        if recursive_octivate:
            self.octivate(recursive_octivate=True, **kwargs)

    def setFiles(self):
        f = inspect.getfile(self.__class__)
        a = os.path.abspath(f)
        p = os.path.dirname(a)
        self.path = p.replace("\\", "/")

        for f in os.listdir(self.path):
            p = f"{self.path}/{f}"
            self.m_files[f] = p

    def addView(
            self, 
            *args,
            view=None, 
            **kwargs
            )->None:
        if not view: return
        view.setManager(self)
        if self.checkProp("setParent", view):
            view.setParent(self)

    def setView(
            self, 
            *args,
            view=None, 
            **kwargs
            )->None:
        if not view: return
        self.m_view = view
        if self.checkProp("setFocus", view):
            view.setFocus()
