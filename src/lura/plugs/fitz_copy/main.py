from plug import Plug, deleg

class FitzCopy(Plug):

    @deleg('clone@(normal)[FitzView]')
    def activate(self, view, **kwargs):
        if view:
            copy = self.app.buffman.createViewClass(
                    view.__class__, 
                    config=view.config())
            copy.setModel(view.model())
            copy.setManager(view.manager())

            zoom=self.app.delegman.delegate(
                    mode='normal',
                    view=view,
                    action='zoomState',
                    data={'view': view})

            if zoom:
                zoom=self.app.delegman.delegate(
                        mode='normal', 
                        view=copy, 
                        action='zoom',
                        data=zoom)

            goTo=self.app.delegman.delegate(
                    mode='normal', 
                    view=view,
                    action='goToState',
                    data={'view': view})
            if goTo:
                goTo=self.app.delegman.delegate(
                        mode='normal',
                        view=copy,
                        action='goTo',
                        data=goTo)
            return copy
