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
                return self.createElement(annotation)

    def updAnnotate(self, element=None, **kwargs):
        model=self.source()
        annotator=self.m_agent.getAgent(model=model)
        if annotator and element:
            self.delAnnotate(element=element)
            self.addAnnotate(**kwargs)

    def delAnnotate(self, element=None, data=None, **kwargs):
        model=self.source()
        annotator=self.m_agent.getAgent(model=model)
        if annotator:
            if not element and data:
                metadata = data.get("metadata")
                element = self.getAnnotate(metadata)
            if element:
                data=element.data()
                annotator.deannotate(model, data, **kwargs)
                return self.delElement(element)

    def getAnnotate(self, value, by="metadata", **kwargs):
        return self.getElement(value, by=by, **kwargs)
