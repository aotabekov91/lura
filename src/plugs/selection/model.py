from PyQt6 import QtCore

from plug_qt import vimo
from plug import Element, hashdict

class SelectionElement(Element, QtCore.QObject):

    def setup(self):
        super().setup()
        self.m_data=hashdict()

    def clear(self):
        self.m_data=hashdict()

    def value(self, key, default=None):
        return self.m_data.get(key, default)

    def setValue(self, key, value):
        self.m_data[key]=value

    def get(self, key, default=None):
        return self.m_data.get(key, default)

    def set(self, key, value):
        self.m_data[key]=value

    def __getitem__(self, key):
        return self.value(key)

    def __setitem__(self, key, value):
        self.setValue(key, value)

    def __bool__(self):
        if self.m_data:
            return True
        return False

class SelectionModel(vimo.Model, QtCore.QObject):

    element_class=SelectionElement

    def __init__(self, agent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.m_agent=agent
        self.m_selection=SelectionElement(model=self)

    def createSelection(self, data={}):
        selection=SelectionElement(model=self)
        if data:
            data=hashdict(data)
            selection.setData(data)
        return selection

    def setSelection(self, selection, view=None):
        self.m_selection=selection
        if view:
            selector=self.m_agent.getAgent(view=view)
            selector.select(view, self.m_selection)

    def updateSelection(self, **kwargs):
        for key, value in kwargs.items():
            self.m_selection.setValue(key, value)
        view=self.source()
        model=view.model()
        if model:
            self.m_selection.setValue('kind', model.kind)
            self.m_selection.setValue('source_id', model.id())
        selector=self.m_agent.getAgent(view=view)
        selector.select(view, self.m_selection)

    def clearSelection(self, **kwargs):
        view=self.source()
        self.m_selection.clear()
        selector=self.m_agent.getAgent(view=view)
        selector.select(view, self.m_selection)

    def getSelection(self, **kwargs):
        return self.m_selection
