from plug import Plug, tag, deleg

class Visual(Plug):

    @deleg('visual@(any)')
    @tag('<c-v>(normal)')
    def activate(self, view=None, submode=None, **kwargs):
        super().activate()
        if not view:
            view=self.app.stateman.view()
        self.app.stateman.activate(
                view=view,
                moder=self,
                mode='visual',
                submode=submode,
                **kwargs)
        data=kwargs.copy()
        data['view']=view
        self.app.delegman.delegate(
                mode='visual', 
                submode=submode, 
                action='activate',
                data=data)

    @deleg('normal@(visual)')
    @tag(['<c-v>/<c-[>(visual[None])', '<escape>(visual)'])
    def octivate(self, view=None, submode=None, **kwargs):
        super().octivate()
        if not view:
            view=self.app.stateman.view()
        if not submode:
            submode=self.app.stateman.submode()
        data=kwargs.copy()
        data['view']=view
        self.app.delegman.delegate(
                mode='visual', 
                submode=submode, 
                action='octivate',
                data=data)
        self.app.stateman.activate()
