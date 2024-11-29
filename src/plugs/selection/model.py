from PyQt6 import QtCore

from plug_qt import vimo
from plug import Element, hashdict

class SelectionElement(Element, QtCore.QObject):

    def setup(self):
        super().setup()
        self.m_data=hashdict()

    def clear(self):
        self.m_data=hashdict()

class SelectionModel(vimo.Model, QtCore.QObject):

    element_class=SelectionElement

    def __init__(self, agent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.m_agent=agent
        self.m_selection=SelectionElement()

    def setSelection(self, selection=None, **kwargs):
        if selection:
            view=self.source()
            model=view.model()
            self.m_selection=selection
            if view:
                selector=self.m_agent.getAgent(view=view)
                selector.select(view, self.m_selection)
        elif kwargs:
            self.updateSelection(**kwargs)
        else:
            self.clearSelection(**kwargs)

    def updateSelection(self, **kwargs):
        for key, value in kwargs.items():
            self.m_selection[key]=value
        view=self.source()
        # model=view.model()
        # if model:
        #     self.m_selection['kind']=model.kind
        #     self.m_selection['source_id']=model.id()
        selector=self.m_agent.getAgent(view=view)
        selector.select(view, self.m_selection)

    def clearSelection(self, **kwargs):
        view=self.source()
        self.m_selection=self.createSelection()
        selector=self.m_agent.getAgent(view=view)
        selector.select(view, self.m_selection)

    def getSelection(self, **kwargs):
        return self.m_selection

    def createSelection(self, data={}, **kwargs):
        selection=SelectionElement()
        view=self.source()
        model=view.model()
        data=hashdict(data)
        data['kind']=model.kind
        data['source_id']=model.id()
        selection.setData(data)
        return selection
