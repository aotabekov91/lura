from plug import Plug

class FitzHighlight(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addToHighlight()
        else:
            self.app.appSoonStarts.connect(
                    self.addToHighlight)

    def addToHighlight(self):
        highlighter=self.app.plugman.plugs.get('Highlight')
        annotator=self.app.plugman.plugs.get('FitzAnnotate')
        if highlighter and annotator:
            highlighter.addHighlighter('FitzView', self)

    def activate(self, view, xrange=[1]):
        selection=view.selection()
        annotator=self.app.plugman.plugs.get('FitzAnnotate')
        if selection:
            annotator.annotate(view, selection)

    def octivate(self, view, **kwargs):
        raise
