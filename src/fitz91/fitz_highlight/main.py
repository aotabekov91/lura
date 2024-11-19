from plug import Plug

class FitzHighlight(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.getPlug('Highlight')
        if holder:
            holder.addAgent('FitzView', self)

    def activate(self, view, selection=None, **kwargs):
        selector=self.app.plugman.getPlug('Selection')
        if not selection:
            selection=selector.selection(view)
        if selection:
            model=view.model()
            data=selection.data()
            selection['annotation_kind']='highlight'
            annotator=self.app.plugman.getPlug('Annotate')
            annotation_model=annotator.getModel(model)
            annotation_model.addAnnotate(data=data)
            selector.cleanUpSelection(view)
        return selection

    def octivate(self):
        raise
