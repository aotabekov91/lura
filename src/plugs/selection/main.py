from PyQt6 import QtCore

from plug import Plug, tag

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
        self.cleanUpWanted.connect(self.cleanUpSelection)
        self.app.buffman.viewCreated.connect(self.createModel)

    def select(self, view, **kwargs):
        selection_model=self.getModel(view)
        if selection_model:
            selection_model.updateSelection(**kwargs)

    def deselect(self, view, **kwargs):
        selection_model=self.getModel(view)
        if selection_model:
            selection_model.clearSelection(**kwargs)

    def selection(self, view, **kwargs):
        selection_model=self.getModel(view)
        if selection_model:
            return selection_model.getSelection(**kwargs)

    @tag('<escape>(normal)')
    def cleanUpSelection(self, view=None):
        if not view:
            view=self.app.stateman.view()
        self.deselect(view)

    def addAgent(self, name, agent):
        self.m_agents[name]=agent

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
