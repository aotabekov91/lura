from PyQt6 import QtCore

from plug import Plug, tag

from .model import AnnotateModel

class Annotate(Plug, QtCore.QObject):

    modelCreated=QtCore.pyqtSignal(object)

    def setup(self):
        super().setup()
        self.m_models={}
        self.m_agents={}
        self.app.buffman.modelCreated.connect(
                self.createModel)

    def addAgent(self, name, annotator):
        self.m_agents[name]=annotator

    def getAgent(self, name=None, model=None):
        if model and not name:
            name=model.__class__.__name__
        return self.m_agents.get(name, None)

    def getModel(self, model):
        return self.m_models.get(model)

    def createModel(self, model):
        annotation_model=AnnotateModel(
                self, source=model)
        self.modelCreated.emit(annotation_model)
        self.m_models[model]=annotation_model
        return annotation_model

    @tag(["<c-a>(normal/visual[any])", "<c-a>/<c-[>/<escape>(annotate)"])
    def toggle(self):
        view=self.app.stateman.view()
        model=view.model()
        annotator=self.getAgent(model=model)
        if annotator:
            self.app.stateman.activate(
                    mode="annotate", toggle_mode=True)

    def activate(self, action=None, model=None, selection=None, **kwargs):
        annotation_model=self.getModel(model)
        if selection and annotation_model:
            data=selection.data()
            if action=='add':
                kind=selection.__class__.__name__
                if kind=='AnnotateElement':
                    annotation_model.updAnnotate(data=data, element=selection)
                else:
                    annotation_model.addAnnotate(data=data)
            elif action=='del':
                    annotation_model.delAnnotate(element=selection)

    @tag("d(annotate)")
    def deannotate(self, view=None, selection=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        selector=self.app.plugman.getPlug('Selection')
        if not selection and selector:
            selection=selector.selection(view)
        if selection:
            model=view.model()
            self.activate(action='del', model=model, selection=selection)
            if selector:
                selector.clear(view)
        self.toggle()
