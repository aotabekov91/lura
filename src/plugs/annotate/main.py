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

    def annotate(self, data={}, model=None, view=None):
        if not model and view: 
            model=view.model()
        annotator=self.getAgent(model=model)
        annotation_model=self.getModel(model)
        print(model, annotation_model)
        if annotator and annotation_model:
            annotation=annotator.annotate(
                    model, data, view=view)
            if annotation:
                annotation_model.addAnnotate(annotation)

    def denotate(self, view, data):
        pass

    def renotate(self, view, data):
        pass

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
                source=model)
        self.modelCreated.emit(annotation_model)
        self.m_models[model]=annotation_model
        return model

    @tag(["<c-a>(normal)", "<c-a>/<c-[>/<escape>(annotate)"])
    def toggle(self):
        view=self.app.stateman.view()
        annotator=self.getAgent(view=view)
        if annotator:
            self.app.stateman.toggle("annotate")
