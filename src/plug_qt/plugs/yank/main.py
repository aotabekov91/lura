from plug import Plug, tag

class Yank(Plug):

    @tag('yp(normal/visual)')
    def yankPath(self, view=None, **kwargs):
        # todo
        pass

    @tag('ys(normal/visual)')
    def yankSelection(self, view=None, **kwargs):
        view=view or self.app.stateman.view()
        if view:
            selection=self.app.delegman.delegate(
                    mode='any',
                    action='getSelection', 
                    data={'view': view},
                    add_fields=[]
                    )
            if selection:
                self.app.delegman.delegate(
                        mode='normal',
                        view=view,
                        add_fields=[],
                        action='yankSelection',
                        data={'view': view, 'selection': selection})
