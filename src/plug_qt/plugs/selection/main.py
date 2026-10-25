from PyQt6 import QtCore

from plug import Plug, deleg

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

    @deleg('setSelection@(any)')
    def setSelection(self, view=None, **kwargs):
        model=self.getModel(view)
        if model:
            model.set(**kwargs)

    @deleg('updateSelection@(any)')
    def updateSelection(self, view=None, **kwargs):
        model=self.getModel(view)
        if model:
            model.update(**kwargs)

    @deleg('clearSelection@(any)')
    def clearSelection(self, view=None, **kwargs):
        model=self.getModel(view)
        if model:
            model.clear(**kwargs)

    @deleg('getSelection@(any)')
    def getSelection(self, view=None, **kwargs):
        model=self.getModel(view=view)
        if model:
            return model.get(**kwargs)

    @deleg('createSelection@(any)')
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
