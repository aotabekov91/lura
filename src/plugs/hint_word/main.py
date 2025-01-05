from plug import Plug, tag

class WordHint(Plug):

    def setup(self):
        super().setup()
        self.m_agents={}
        if self.app.running:
            self.addSubmode()
        else:
            self.app.appIsLaunched.connect(
                    self.addSubmode)

    def addSubmode(self):
        holder=self.app.plugman.getPlug('Hint')
        if holder:
            holder.addSubmode('word', self)

    @tag("<c-w>(hint)")
    def activate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent=self.app.delegman.getAgent(
                'hint', 'word', view, delegate='view')
        if agent:
            self.app.stateman.setSubmode(
                    submode="word", submoder=self)
            functor=agent.get('start', None)
            if functor:
                functor(view=view, **kwargs)

    @tag("<c-w>/<c-[>/<escape>(hint[word])")
    def octivate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        self.app.stateman.setSubmode()
        functor=self.app.delegman.getAgent(
                'hint', 'word', view, 'finish') 
        if functor:
            functor(view=view, **kwargs)
