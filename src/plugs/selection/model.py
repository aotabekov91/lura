from PyQt6 import QtCore

from plug import Element
from plug_qt import vimo

class SelectionElement(Element, QtCore.QObject):
    pass

class SelectionModel(vimo.Model, QtCore.QObject):

    element_class=SelectionElement
    def __init__(self, agent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.m_agent=agent

    def addSelection(self, data={}, **kwargs):
        view=self.source()
        selector=self.m_agent.getAgent(view=view)
        if selector:
            selection=selector.select(
                    view, data, **kwargs)
            if selection:
                position = selection.get("metadata")
                element = self.getSelection(position)
                if not element:
                    element=self.createElement(selection)
                else:
                    self.updateElement(element, selection)
                return element

    def updateSelection(self, data={}, **kwargs):
        model=self.source()
        selector=self.m_agent.getAgent(model=model)
        if selector:
            annotation=selector.annotate(
                    model, data, **kwargs)
            if annotation:
                position = annotation.get("metadata")
                element = self.getSelection(position)
                if element:
                    self.updateElement(element, annotation)
                return element

    def delSelection(self, element=None, data=None, **kwargs):
        model=self.source()
        selector=self.m_agent.getAgent(model=model)
        if selector:
            if not element and data:
                position = data.get("metadata")
                element = self.getSelection(position)
            if element:
                data=element.data()
                selector.deannotate(model, data, **kwargs)
                return self.delElement(element)

    def getSelection(self, value, by="metadata", **kwargs):
        return self.getElement(value, by=by, **kwargs)
