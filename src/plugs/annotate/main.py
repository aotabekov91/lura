from plug import Plug, tag

class Annotate(Plug):

    def setup(self):
        super().setup()
        self.m_annotators={}

    def addAnnotator(self, name, annotator):
        self.m_annotators[name]=annotator

    def annotator(self, name):
        return self.m_annotators.get(name, None)

    @tag(["<c-a>(normal)", "<c-a>/<c-[>/<escape>(annotate)"])
    def toggle(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        annotator=self.annotator(name)
        if annotator:
            self.app.stateman.toggle("annotate")
