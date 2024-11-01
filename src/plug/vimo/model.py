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
        elements=OrderedDict(),
        **kwargs,
    ):
        self.app = app
        self.m_id = index
        self.m_data = None
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
        for k, v in self.m_config.items():
            setattr(self, k, v)

    def setName(self):
        name = self.__class__.__name__
        name = self.m_name or name
        self.name = self.name or name

    def setKind(self):
        name = self.__class__.__name__
        self.kind = self.kind or name

    def config(self):
        return self.m_config

    def count(self):
        return len(self.m_elements)

    def readSuccess(self):
        return self.m_data is not None

    def modelData(self):
        return self.m_data

    def id(self):
        return self.m_id

    def setId(self, idx):
        self.m_id = idx

    def element(self, idx):
        return self.m_elements.get(idx, None)

    def elements(self):
        return self.m_elements

    def setElements(self, elements):
        self.m_elements = elements

    def __eq__(self, o):
        return o and id(self) == id(o)

    def __hash__(self):
        return id(self) 

    def source(self):
        return self.m_source

    def resetConfigure(self, **kwargs):
        pass

    def load(self):
        self.isLoaded = True

    @classmethod
    def isCompatible(cls, s, **kwargs):
        if type(s) != str:
            return
        if not cls.pattern:
            return
        return re.match(cls.pattern, s, re.I)

    @classmethod
    def getSourceName(cls, source, **kwargs):
        return source

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
        element = self.element_class(
            data=data, index=idx, model=self
        )
        self.addElement(element)
        return element

    def findElement(self, value=None, by=None):
        for idx, e in self.m_elements.items():
            d = e.data()
            if d.get(by) == value:
                return idx, e

    def addElement(self, element):
        idx = element.index()
        self.m_elements[idx] = element
        return element

    def delElement(self, element):
        self.m_elements.pop(element.index(), None)
        return element

    def updateElement(self, element, data):
        element.updateData(data)
        return element

    def getElement(self, value, by="id"):
        elements=self.m_elements.values()
        for element in elements: 
            data = element.data()
            if not by in data:
                continue
            if value != data.get(by, None):
                continue
            return element

    def clearAll(self):
        elems = self.m_elements
        self.m_elements = OrderedDict()
        for e in elems.values():
            self.delElement(e)
