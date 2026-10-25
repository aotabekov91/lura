from plug import Plug, deleg

class FitzYankSelection(Plug):

    @deleg('yankSelection@(normal)[FitzView]')
    def yankSelection(self, view=None, selection=None, **kwargs):
        if selection and view:
            text=selection.get('text', None)
            if text:
                clipboard = self.app.qapp.clipboard()
                clipboard.setText(text)
            selection.clear()
            view.redraw()
            return text
