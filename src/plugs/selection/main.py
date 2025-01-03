from PyQt6 import QtCore

from plug import Plug

from .model import SelectionModel

class Selection(Plug, QtCore.QObject):

    modelCreated=QtCore.pyqtSignal(object)
    cleanUpWanted=QtCore.pyqtSignal(object)

    selected = QtCore.pyqtSignal(object)
    selectionPainted = QtCore.pyqtSignal(
        object, object, object, object)

    def setup(self):
        super().setup()
        self.m_models={}
        self.m_agents={}
        self.m_selection = None
        self.cleanUpWanted.connect(self.clear)
        self.app.buffman.viewCreated.connect(self.createModel)

    def addAgent(self, name, agent):
        self.m_agents[name]=agent

    def select(self, view, **kwargs):
        model=self.getModel(view)
        if model:
            model.set(**kwargs)

    def update(self, view, **kwargs):
        model=self.getModel(view)
        if model:
            model.update(**kwargs)

    def deselect(self, view, **kwargs):
        model=self.getModel(view)
        if model:
            model.clear(**kwargs)

    def selection(self, view, **kwargs):
        model=self.getModel(view)
        if model:
            return model.get(**kwargs)

    def clear(self, view=None):
        if not view:
            view=self.app.stateman.view()
        self.deselect(view)

    def getAgent(self, name=None, view=None):
        if view and not name:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    def getModel(self, model):
        return self.m_models.get(model)

    def createModel(self, view):
        selector=self.getAgent(view=view)
        if selector:
            selection_model=SelectionModel(
                    self, source=view)
            self.m_models[view]=selection_model
            self.modelCreated.emit(selection_model)
            return view

    def create(self, view=None, **kwargs):
        model=self.getModel(view)
        if model:
            return model.create(**kwargs) 

    def activate(self, kind=None, **kwargs):
        if kind=='select':
            raise
