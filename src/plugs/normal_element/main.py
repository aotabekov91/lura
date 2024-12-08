from plug import Plug

class ElementViewNormal(Plug):

    # def setup(self):
    #     super().setup()
    #     if self.app.running:
    #         self.addAgent()
    #     else:
    #         self.app.appSoonStarts.connect(
    #                 self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.getPlug('Normal')
        if holder:
            holder.addAgent('goTo', 'ElementView', self)
            holder.addAgent('close', 'ElementView', self)

    def currentPosition(self, *args, **kwargs):
        return {}

    def close(self, view=None, **kwargs):
        raise

    def goTo(self, view=None, xrange=[1], **kwargs):
        if view:
            id_widget, _=view.widget('id')
            text_widget, _=view.widget('text')
            if id_widget.hasFocus():
                text_widget.setFocus()
            else:
                id_widget.setFocus()

    def activate(self, action=None, **kwargs):
        if action:
            func=getattr(self, action, None)
            if func:
                func(**kwargs)
