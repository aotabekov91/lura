from plug import Plug, tag

class WordHint(Plug):

    def setup(self):
        super().setup()
        self.addAgent()

    def addAgent(self):
        self.app.delegman.addAgent(
                mode='hint', 
                submode='word', 
                action='activate', 
                functor=self.activate)
        self.app.delegman.addAgent(
                mode='hint', 
                submode='word', 
                action='octivate', 
                functor=self.octivate)

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
                    'hint', 'word', view, 'start', data=kwargs) 

    @tag("<c-w>/<c-[>/<escape>(hint[word])")
    def octivate(self, view=None, **kwargs):
        super().octivate()
        if not view:
            view=self.app.stateman.view()
        self.app.stateman.setSubmode()
        self.app.delegman.delegate(
                'hint', 'word', view, 'finish', data=kwargs) 
