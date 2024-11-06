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

    def select(self, item, data, **kwargs):
        if self.checkProp("canSelect", item):
            item.select(data, **kwargs)
            self.m_selection = data

    def deselect(self, *args, **kwargs):
        raise

    def selection(self, view, index=1):
        return self.m_selection

    def clearSelection(self, view):
        items=view.items()
        for item in items.values():
            if self.checkProp("canSelect", item):
                item.select()

    @tag('<c-[>(normal/visual)')
    def cleanUpSelection(self):
        view=self.appstateman.view()
        self.clearSelection(view)
        self.m_selection = None

    def addAgent(self, name, agent):
        self.m_agents[name]=agent

    def getAgent(self, name=None, view=None):
        if view and not name:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    def getModel(self, model):
        return self.m_models.get(model)

    def createModel(self, view):
        selection_model=SelectionModel(
                self, source=view)
        self.modelCreated.emit(selection_model)
        self.m_models[view]=selection_model
        return view
