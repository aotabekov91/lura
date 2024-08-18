from plug import Plug, tag

class Highlight(Plug):

    def setup(self):
        super().setup()
        self.m_highlighters={}

    def addHighlighter(self, name, annotator):
        self.m_highlighters[name]=annotator

    def highlighter(self, name):
        return self.m_highlighters.get(name, None)

    @tag(["<c-h>(annotate)", "<c-h>/<c-[>/<escape>(annotate|highlight)"])
    def toggle(self, xrange=[1]):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        highlighter=self.highlighter(name)
        if highlighter:
            submode=self.app.stateman.toggleSubmode("highlight")
            if submode=='highlight':
                highlighter.activate(view, xrange)
            else:
                highlighter.octivate(view, xrange)
