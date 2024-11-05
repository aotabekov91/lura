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
        if highlighter:
            highlighter.addAgent('FitzView', self)

    def highlight(self, view, data=None, **kwargs):
        if not data:
            data=view.selection()
        if data:
            model=view.model()
            data['annotation_kind']='highlight'
            annotator=self.app.plugman.plugs.get('Annotate')
            annotation_model=annotator.getModel(model)
            annotation_model.addAnnotate(data=data, view=view)
        return data

    def rehighlight(self):
        raise
