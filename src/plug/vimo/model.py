import re
from collections import OrderedDict

from .element import Element


class Model:
    kind = None
    name = None
    wantView = []
    isType = False
    pattern = None
    isLoaded = False
    wantUniqView = False
    element_class = Element

    def __init__(
        self,
        app=None,
        config={},
        name=None,
        index=None,
        source=None,
        render=None,
        parent=None,
        elements=OrderedDict(),
        **kwargs,
    ):
        self.app = app
        self.m_id = index
        self.m_data = None
        self.m_models = {}
        self.m_name = name
        self.m_loaded = False
        self.m_source = source
        self.m_config = config
        self.m_render = render
        self.m_base_model = None
        self.m_elements = elements.copy()
        self.m_kwargs = kwargs
        super().__init__()
        self.setup()

    def setup(self):
        self.updateKlass()
        self.setConf()
        self.setKind()
        self.setName()

    def updateKlass(self):
        ek = self.m_kwargs.get("element_class")
        if ek:
            self.element_class = ek

    def setConf(self):
        c = self.m_config
        for k, v in c.items():
            setattr(self, k, v)

    def setName(self):
        c = self.__class__.__name__
        c = self.m_name or c
        self.name = self.name or c

    def setKind(self):
        c = self.__class__.__name__
        self.kind = self.kind or c

    def addModel(self, name, model):
        self.m_models[name] = model
        self.modelAdded.emit(name, model)

    def submodel(self, name):
        return self.m_models.get(name)

    def config(self):
        return self.m_config

    def setBasemodel(self, model):
        self.m_base_model = model

    def basemodel(self):
        return self.m_base_model

    def render(self):
        return self.m_render

    def count(self):
        return len(self.m_elements)

    def readSuccess(self):
        return self.m_data is not None

    def id(self):
        return self.m_id

    def setId(self, idx):
        self.m_id = idx
        self.idChanged.emit(idx)

    def element(self, idx):
        return self.m_elements.get(idx, None)

    def elements(self):
        return self.m_elements

    def setElements(self, elements):
        self.m_elements = elements

    def __eq__(self, o):
        return o and id(self) == id(o)

    def __hash__(self):
        return hash(self.m_data)

    def source(self):
        return self.m_source

    def resetConfigure(self, **kwargs):
        pass

    def load(self):
        self.isLoaded = True
        self.loaded.emit(self)

    @classmethod
    def isCompatible(cls, s, **kwargs):
        if type(s) != str:
            return
        if not cls.pattern:
            return
        return re.match(cls.pattern, s, re.I)

    @classmethod
    def getSourceName(cls, s, **kwargs):
        return s

    def setProp(self, what, value=True, view=None):
        view=view or self
        setattr(self, what, value)

    def delProp(self, what):
        delattr(self, what)

    def checkProp(self, what, m=None):
        m = m or self
        if type(what) != list:
            what = [what]
        for w in what:
            if not getattr(m, w, False):
                return False
        return True

    def createElement(self, data={}, idx=None):
        if not idx:
            idx = id(data)
        e = self.element_class(
            data=data, index=idx, model=self
        )
        self.elementCreated.emit(e)
        self.addElement(e)
        return e

    def findElement(self, value=None, by=None):
        for idx, e in self.m_elements.items():
            d = e.data()
            if d.get(by) == value:
                return idx, e

    def addElement(self, e):
        idx = e.index()
        self.m_elements[idx] = e
        self.elementAdded.emit(e)
        return e

    def delElement(self, e):
        self.m_elements.pop(e.index(), None)
        self.elementRemoved.emit(e)
        return e

    def getElement(self, value, by="id"):
        for e in self.m_elements.values():
            d = e.data()
            if not by in d:
                continue
            if value != d.get(by, None):
                continue
            return e

    def updateElement(self, e, data):
        e.updateData(data)
        self.elementUpdated.emit(e)
        return e

    def clearAll(self):
        elems = self.m_elements
        self.m_elements = OrderedDict()
        for e in elems.values():
            self.delElement(e)
