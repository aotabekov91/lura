from plug import Plug

class FitzTextize(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.plugs.get('Textize')
        if holder:
            holder.addAgent('FitzView', self)

    def activate(self, view, selection=None, **kwargs):
        if not selection:
            selector=self.app.plugman.plugs.get('Selection')
            selection=selector.selection(view)
        if selection:
            model=view.model()
            selection.setValue('annotation_kind', 'text')
            annotator=self.app.plugman.plugs.get('Annotate')
            annotation_model=annotator.getModel(model)

            annotation_model.addAnnotate(data=selection, view=view)
        return selection

    def octivate(self):
        raise
