from PyQt6 import QtCore

from plug import Element
from plug_qt import vimo

class AnnotateElement(Element, QtCore.QObject):
    pass

class AnnotateModel(vimo.Model, QtCore.QObject):

    element_class=AnnotateElement

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app=app

    def add(self, model=None, **kwargs):
        if model:
            annotation=self.app.delegman.delegate(
                    mode='annotate', 
                    model=model,
                    action='annotate',
                    data=kwargs)
            agent=self.app.delegman.getAgent(
                    mode='annotate', 
                    model=model,
                    action='remove',)
            if annotation:
                return self.createElement(annotation)

    def update(self, model=None, annotation=None, **kwargs):
        if annotation and model:
            kwargs['annotation']=annotation
            self.app.delegman.delegate(
                    mode='annotate', 
                    model=model, 
                    action='remove',
                    data=kwargs)
            return self.add(view=view, **kwargs)

    def remove(self, model=None, view=None, annotation=None, data=None, **kwargs):
        if not annotation and data:
            metadata = data.get("metadata")
            annotation = self.getAnnotate(metadata)
        if annotation and model:
            data=annotation.data()
            self.app.delegman.delegate(
                    mode='annotate', 
                    model=model,
                    action='remove',
                    data={'model': model, 'data': data})
            agent=self.app.delegman.getAgent(
                    mode='annotate', 
                    model=model,
                    action='remove',)
            return self.delElement(annotation)

    def get(self, value, by="metadata", **kwargs):
        return self.getElement(value, by=by, **kwargs)
