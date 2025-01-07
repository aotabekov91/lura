from plug import Plug, tag, deleg

class WordHint(Plug):

    @deleg('activate@(hint[word])')
    @tag("<c-w>(hint)")
    def activate(self, view=None, **kwargs):
        super().activate()
        if not view:
            view=self.app.stateman.view()
        agent=self.app.delegman.getAgent(
                'hint', 'word', view, delegate='view')
        if agent:
            self.app.stateman.setSubmode(
                    submode="word", submoder=self)
            self.app.delegman.delegate(
                    mode='hint', 
                    submode='word', 
                    view=view, 
                    action='activate', 
                    data=kwargs) 

    @deleg('octivate@(hint[word])')
    @tag("<c-w>/<c-[>/<escape>(hint[word])")
    def octivate(self, view=None, **kwargs):
        super().octivate()
        if not view:
            view=self.app.stateman.view()
        self.app.stateman.setSubmode()
        self.app.delegman.delegate(
                mode='hint', 
                submode='word', 
                view=view, 
                action='octivate', 
                data=kwargs) 
