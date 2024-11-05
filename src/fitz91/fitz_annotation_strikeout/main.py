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

    def activate(self, view, data=None, **kwargs):
        if not data:
            data=view.selection()
        if data:
            model=view.model()
            data['annotation_kind']='strikeout'
            annotator=self.app.plugman.plugs.get('Annotate')
            annotation_model=annotator.getModel(model)
            annotation_model.addAnnotate(data=data, view=view)
        return data

    def octivate(self):
        raise
