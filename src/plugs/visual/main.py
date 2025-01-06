from plug import Plug, tag

class Visual(Plug):

    def setup(self):
        super().setup()
        self.addAgent()

    def addAgent(self):
        self.app.delegman.addAgent(
                None, None, None, 'visual', self.activate)
        self.app.delegman.addAgent(
                'visual', None, None, 'normal', self.octivate)

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

    @tag('<c-v>/<escape>(visual[any])')
    def octivate(self, view=None, submode=None, **kwargs):
        super().octivate()
        if not view:
            view=self.app.stateman.view()

        if not submode:
            submode=self.app.stateman.submode()
        data=kwargs.copy()
        data['view']=view
        self.app.delegman.delegate(
                mode='hint', 
                submode=submode, 
                action='octivate',
                data=data)
        self.app.stateman.activate()
