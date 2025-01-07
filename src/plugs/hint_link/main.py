from plug import Plug, tag, deleg

class LinkHint(Plug):

    @deleg('activate@(hint[link])')
    @tag("<c-l>(hint)")
    def activate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent=self.app.delegman.getAgent(
                'hint', 'link', view, delegate='view')
        if agent:
            self.app.stateman.setSubmode(
                    submode="link", submoder=self)
            self.app.delegman.delegate(
                    mode='hint', 
                    submode='link', 
                    view=view, 
                    action='activate', 
                    data=kwargs) 

    @deleg('octivate@(hint[link])')
    @tag("<c-l>/<c-[>/<escape>(hint[word])")
    def octivate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        self.app.stateman.setSubmode()
        self.app.delegman.delegate(
                mode='hint', 
                submode='link', 
                view=view, 
                action='octivate', 
                data=kwargs) 
