from PyQt6 import QtCore

from plug import Element
from plug_qt import vimo

class SelectionElement(Element, QtCore.QObject):

    def setup(self):
        super().setup()
        self.m_values={}

    def clear(self):
        self.m_values={}

    def values(self):
        return self.m_values

    def value(self, name, default=None):
        return self.m_values.get(name, default)

    def setValue(self, name, value):
        self.m_values[name]=value

    def __bool__(self):
        if self.m_values:
            return True
        return False

class SelectionModel(vimo.Model, QtCore.QObject):

    element_class=SelectionElement

    def __init__(self, agent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.m_agent=agent
        self.m_selection=SelectionElement(model=self)

    def updateSelection(self, **kwargs):
        view=self.source()
        selector=self.m_agent.getAgent(view=view)
        for key, value in kwargs.items():
            self.m_selection.setValue(key, value)
        selector.select(view, self.m_selection)

    def clearSelection(self, **kwargs):
        view=self.source()
        self.m_selection.clear()
        selector=self.m_agent.getAgent(view=view)
        selector.select(view, self.m_selection)

    def getSelection(self, **kwargs):
        return self.m_selection
