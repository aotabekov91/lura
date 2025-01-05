from plug import Plug

class ElementViewNormal(Plug):

    def addAgent(self):
        self.app.delegman.addAgent(
                'normal', None, 'goTo', 'ElementView', self.goTo)
        self.app.delegman.addAgent(
                'normal', None, 'close', 'ElementView', self.close)

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
