from plug import Plug, tag

class Paste(Plug):

    @tag('ps(normal/visual)')
    def pasteSelection(self, view=None, **kwargs):
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
                        action='pasteSelection',
                        data={'view': view, 'selection': selection})
