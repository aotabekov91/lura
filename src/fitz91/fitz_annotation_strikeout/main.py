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
        holder=self.app.plugman.getPlug('Strikeout')
        if holder:
            holder.addAgent('FitzView', self)

    def activate(self, view, selection=None, **kwargs):
        selector=self.app.plugman.getPlug('Selection')
        if not selection:
            selection=selector.selection(view)
        if selection:
            model=view.model()
            selection['annotation_kind']='strikeout'
            annotator=self.app.plugman.getPlug('Annotate')
            annotation_model=annotator.getModel(model)
            data=selection.data()
            annotation_model.addAnnotate(data=data)
            selector.clear(view)
        return selection

    def octivate(self):
        raise
