from plug import Plug

class FitzStrikeout(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.plugs.get('Strikeout')
        if holder:
            holder.addAgent('FitzView', self)

    def activate(self, view, selection=None, **kwargs):
        selector=self.app.plugman.plugs.get('Selection')
        if not selection:
            selection=selector.selection(view)
        if selection:
            model=view.model()
            selection['annotation_kind']='strikeout'
            annotator=self.app.plugman.plugs.get('Annotate')
            annotation_model=annotator.getModel(model)
            data=selection.data()
            annotation_model.addAnnotate(data=data)
            selector.cleanUpSelection(view)
        return selection

    def octivate(self):
        raise
