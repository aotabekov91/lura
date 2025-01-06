from plug import Plug, tag

class LinkHint(Plug):

    def setup(self):
        super().setup()
        self.addAgent()

    def addAgent(self):
        self.app.delegman.addAgent(
                mode='hint', 
                submode='link', 
                action='activate', 
                functor=self.activate)
        self.app.delegman.addAgent(
                mode='hint', 
                submode='link', 
                action='octivate', 
                functor=self.octivate)

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
                    'hint', 'link', view, 'start', data=kwargs) 

    @tag("<c-l>/<c-[>/<escape>(hint[word])")
    def octivate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        self.app.stateman.setSubmode()
        self.app.delegman.delegate(
                'hint', 'link', view, 'finish', data=kwargs) 
