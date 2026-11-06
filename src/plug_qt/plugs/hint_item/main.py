from plug import Plug, tag, deleg

class ItemHint(Plug):

    @deleg('activate@(hint[item])')
    @tag("<c-i>(hint)")
    def activate(self, view=None, **kwargs):
        super().activate()
        view=view or self.app.stateman.view()
        agent=self.app.delegman.getAgent(
                'hint', 'item', view, delegate='view')
        if agent:
            self.app.stateman.setSubmode(
                    submode="item", submoder=self)
            self.app.delegman.delegate(
                    mode='hint', 
                    submode='item', 
                    view=view, 
                    action='activate', 
                    data=kwargs) 

    @deleg('octivate@(hint[item])')
    @tag("<c-b>/<c-[>/<escape>(hint[item])")
    def octivate(self, view=None, **kwargs):
        super().octivate()
        view=view or self.app.stateman.view()
        self.app.stateman.setSubmode()
        self.app.delegman.delegate(
                mode='hint', 
                submode='item', 
                view=view, 
                action='octivate', 
                data=kwargs) 
