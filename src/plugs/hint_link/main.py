from plug import Plug, tag

class LinkHint(Plug):

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
            holder.addSubmode('link', self)

    @tag("<c-l>(hint)")
    def activate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent=self.app.delegman.getAgent(
                'hint', 'link', view, delegate='view')
        if agent:
            self.app.stateman.setSubmode(
                    submode="link", submoder=self)
            functor=agent.get('start', None)
            if functor:
                functor(view=view, **kwargs)

    @tag("<c-l>/<c-[>/<escape>(hint[word])")
    def octivate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        self.app.stateman.setSubmode()
        functor=self.app.delegman.getAgent(
                'hint', 'link', view, 'finish') 
        if functor:
            functor(view=view, **kwargs)
