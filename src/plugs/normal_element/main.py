from plug import Plug, deleg

class ElementViewNormal(Plug):

    def currentPosition(self, *args, **kwargs):
        return {}

    @deleg('close@(normal)[ElementView])')
    def close(self, view=None, **kwargs):
        raise

    @deleg('goTo@(normal)[ElementView]')
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
