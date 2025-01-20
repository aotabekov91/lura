from plug import Plug, deleg

class NormalListViewGoTo(Plug):

    @deleg('goTo@(normal)[ListView/ElementListView]')
    def goTo(self, view=None, action=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        if view and action:
            functor=getattr(view, action, None)
            if functor:
                functor(**kwargs)
