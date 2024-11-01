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
        print(model, name, self.m_agents)
        return self.m_agents.get(name, None)

    def getModel(self, model):
        return self.m_models.get(model)

    def createModel(self, model):
        annotation_model=AnnotateModel(
                self, source=model)
        self.modelCreated.emit(annotation_model)
        self.m_models[model]=annotation_model
        return model

    @tag(["<c-a>(normal)", "<c-a>/<c-[>/<escape>(annotate)"])
    def toggle(self):
        view=self.app.stateman.view()
        model=view.model()
        annotator=self.getAgent(model=model)
        if annotator:
            self.app.stateman.toggle("annotate")
