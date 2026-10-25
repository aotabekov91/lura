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

    def __init__(self, app, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app=app
        self.m_selection=SelectionElement()

    def set(self, selection=None, **kwargs):
        if selection:
            view=self.source()
            self.m_selection=selection
            self.app.delegman.delegate(
                    view=view, 
                    action='select', 
                    data={'selection': selection})
        elif kwargs:
            self.update(**kwargs)
        else:
            self.clear(**kwargs)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            self.m_selection[key]=value
        view=self.source()
        self.app.delegman.delegate(
                view=view,
                action='select', 
                data={'selection': self.m_selection})

    def clear(self, **kwargs):
        view=self.source()
        self.m_selection=self.create()
        self.app.delegman.delegate(
                view=view, 
                action='select', 
                data={'selection': self.m_selection})

    def get(self, **kwargs):
        return self.m_selection

    def create(self, data={}, **kwargs):
        selection=SelectionElement()
        view=self.source()
        model=view.model()
        data=hashdict(data)
        data['kind']=model.kind
        data['source_id']=model.id()
        selection.setData(data)
        return selection
