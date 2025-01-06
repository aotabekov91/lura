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

    def add(self, view=None, **kwargs):
        annotation=self.app.delegman.delegate(
                mode='annotate', 
                view=view, 
                action='annotate',
                data=kwargs)
        if annotation:
            return self.createElement(annotation)

    def update(self, view=None, annotation=None, **kwargs):
        if annotation:
            kwargs['annotation']=annotation
            self.app.delegman.delegate(
                    mode='annotate', 
                    view=view, 
                    action='remove',
                    data=kwargs)
            return self.add(view=view, **kwargs)

    def remove(self, view=None, annotation=None, data=None, **kwargs):
        if not annotation and data:
            metadata = data.get("metadata")
            annotation = self.getAnnotate(metadata)
        if annotation:
            data=annotation.data()
            self.app.delegman.delegate(
                    mode='annotate', 
                    view=view, 
                    action='remove',
                    data={'view': view, 'data': data})
            return self.delElement(annotation)

    def get(self, value, by="metadata", **kwargs):
        return self.getElement(value, by=by, **kwargs)
