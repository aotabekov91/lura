from plug import Plug, tag

class Hint(Plug):

    alpha: str = "abcdefghijklmnopqrstuvwxyz"

    def setup(self):
        super().setup()
        self.m_agents={}

    def addAgent(self, name, hinter):
        self.m_agents[name]=hinter

    def getAgents(self, name):
        return self.m_agents.get(name, None)

    @tag(["<c-f>(normal)", "<c-f>/<c-[>(hint)"])
    def toggle(self):
        self.app.stateman.activate(
                mode="hint", delisten=True, toggle_mode=True)

    @tag("<escape>(hint[any])")
    def octivate(self):
        self.app.stateman.activate()

    def generateHints(self, alist, kind="letter"):
        list_len = len(alist)
        alpha_len = len(self.alpha)
        number, hints = 0, {} 
        while alpha_len**number < list_len:
            number += 1
        number = max(number, 1)
        for num, data in enumerate(alist):
            if kind == "letter":
                hint = self.mapToLetters(num, number)
            else:
                hint = str(num + 1)
            hints[hint]=data
        return number, hints

    def mapToLetters(self, num, number):
        hint = []
        for _ in range(number):
            hint.append(self.alpha[num % len(self.alpha)])
            num = num // len(self.alpha)
        return "".join(reversed(hint))
