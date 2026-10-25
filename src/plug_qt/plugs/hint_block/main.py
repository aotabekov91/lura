from plug import Plug, tag, deleg

class BlockHint(Plug):

    @deleg('activate@(hint[block])')
    @tag("<c-w>(hint)")
    def activate(self, view=None, **kwargs):
        super().activate()
        if not view:
            view=self.app.stateman.view()
        agent=self.app.delegman.getAgent(
                'hint', 'block', view, delegate='view')
        print(agent)
        if agent:
            self.app.stateman.setSubmode(
                    submode="block", submoder=self)
            self.app.delegman.delegate(
                    mode='hint', 
                    submode='block', 
                    view=view, 
                    action='activate', 
                    data=kwargs) 

    @deleg('octivate@(hint[block])')
    @tag("<c-b>/<c-[>/<escape>(hint[block])")
    def octivate(self, view=None, **kwargs):
        super().octivate()
        if not view:
            view=self.app.stateman.view()
        self.app.stateman.setSubmode()
        self.app.delegman.delegate(
                mode='hint', 
                submode='block', 
                view=view, 
                action='octivate', 
                data=kwargs) 
