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
        self.cleanUpWanted.connect(self.clear)
        self.app.buffman.viewCreated.connect(self.createModel)
        self.addAgent()

    def addAgent(self):
        self.app.delegman.addAgent(
                action='setSelection', functor=self.setSelection)
        self.app.delegman.addAgent(
                action='getSelection', functor=self.getSelection)
        self.app.delegman.addAgent(
                action='updateSelection', functor=self.updateSelection)
        self.app.delegman.addAgent(
                action='clearSelection', functor=self.clearSelection)
        self.app.delegman.addAgent(
                action='createSelection', functor=self.createSelection)

    def setSelection(self, view=None, **kwargs):
        model=self.getModel(view)
        if model:
            model.set(**kwargs)

    def updateSelection(self, view=None, **kwargs):
        model=self.getModel(view)
        if model:
            model.update(**kwargs)

    def clearSelection(self, view=None, **kwargs):
        model=self.getModel(view)
        if model:
            model.clear(**kwargs)

    def getSelection(self, view=None, **kwargs):
        model=self.getModel(view=view)
        if model:
            return model.get(**kwargs)

    def createSelection(self, view=None, **kwargs):
        model=self.getModel(view)
        if model:
            return model.create(**kwargs) 

    def clear(self, view=None):
        if not view:
            view=self.app.stateman.view()
        self.clearSelection(view=view)

    def getModel(self, view=None):
        return self.m_models.get(view, None)

    def createModel(self, view):
        agent=self.app.delegman.getAgent(
                view=view, action='select')
        if agent:
            model=SelectionModel(app=self.app, source=view)
            self.m_models[view]=model
            self.modelCreated.emit(model)
            return view
