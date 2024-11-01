from PyQt6 import QtCore

from plug import Element
from plug_qt import vimo

class AnnotateElement(Element, QtCore.QObject):
    pass

class AnnotateModel(vimo.Model, QtCore.QObject):

    element_class=AnnotateElement
    def __init__(self, agent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.m_agent=agent

    def addAnnotate(self, data={}, **kwargs):
        model=self.source()
        annotator=self.m_agent.getAgent(model=model)
        if annotator:
            annotation=annotator.annotate(
                    model, data, **kwargs)
            if annotation:
                position = annotation.get("metadata")
                element = self.getAnnotate(position)
                if not element:
                    element=self.createElement(annotation)
                else:
                    self.updateElement(element, annotation)
                return element

    def updateAnnotate(self, data={}, **kwargs):
        model=self.source()
        annotator=self.m_agent.getAgent(model=model)
        if annotator:
            annotation=annotator.annotate(
                    model, data, **kwargs)
            if annotation:
                position = annotation.get("metadata")
                element = self.getAnnotate(position)
                if element:
                    self.updateElement(element, annotation)
                return element

    def delAnnotate(self, element=None, data=None):
        if not element and data:
            position = data.get("metadata")
            element = self.getAnnotate(position)
        return self.delElement(element)

    def getAnnotate(self, data, by="metadata"):
        return self.getElement(data, by=by)
