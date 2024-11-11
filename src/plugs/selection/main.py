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

    def select(self, view, data, **kwargs):
        selection_model=self.getModel(view)
        if selection_model:
            selection_model.addSelection(data)

    def deselect(self, view, **kwargs):
        selection_model=self.getModel(view)
        if selection_model:
            selection_model.addSelection(data)
        agent=self.getAgent(view=view)
        if agent:
            agent.deselect(view)

    def selection(self, view, index=None):
        return self.m_selection

    @tag('<c-[>(normal/visual)')
    def cleanUpSelection(self):
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
