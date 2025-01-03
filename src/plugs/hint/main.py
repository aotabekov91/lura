from plug import Plug, tag

class Hint(Plug):

    alpha: str = "abcdefghijklmnopqrstuvwxyz"

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, action, name, hinter):
        if not action in self.m_agents:
            self.m_agents[action]={}
        self.m_agents[action][name]=hinter

    def getAgent(self, action=None, view=None):
        actions=self.m_agents.get(action, {})
        if view and actions:
            for klass in view.__class__.__mro__:
                name=klass.__name__
                agent=actions.get(name)
                if agent: 
                    return agent

    def generateHints(self, alist, kind="letter"):

        def mapToLetters(num, number):
            hint = []
            for _ in range(number):
                hint.append(self.alpha[num % len(self.alpha)])
                num = num // len(self.alpha)
            return "".join(reversed(hint))

        list_len = len(alist)
        alpha_len = len(self.alpha)
        number, hints = 0, {} 
        while alpha_len**number < list_len:
            number += 1
        number = max(number, 1)
        for num, data in enumerate(alist):
            if kind == "letter":
                hint = mapToLetters(num, number)
            else:
                hint = str(num + 1)
            hints[hint]=data
        return number, hints

    def activate(self, action=None, kind=None, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent=self.getAgent(action=action, view=view)
        if agent:
            self.app.stateman.setSubmode(
                    submode=kind, submoder=agent)
            agent.activate(
                    action=action, kind=kind, view=view, **kwargs)

    @tag("<c-f>(normal)")
    def activateHint(self, **kwargs):
        super().activate()
        self.app.stateman.activate(
                mode="hint", delisten=True, **kwargs)

    @tag("<escape>/<c-f>/<c-[>(hint[any])")
    def octivate(self, view=None, **kwargs):
        super().octivate()
        submoder=self.app.stateman.submoder()
        if submoder:
            submoder.octivate(view=view, **kwargs)
        self.app.stateman.activate()

    @tag("<c-w>(hint)")
    def hintWords(self, **kwargs):
        self.activate(action='hintWord', kind='word', **kwargs)

    @tag("<c-l>(hint)")
    def hintLinks(self, *args, **kwargs):
        self.activate(action='hintLink', kind='link', **kwargs)
