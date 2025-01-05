from plug import Plug, tag

class Hint(Plug):

    alpha: str = "abcdefghijklmnopqrstuvwxyz"

    def setup(self):
        super().setup()
        self.m_submodes={}

    def addSubmode(self, name, agent):
        self.m_submodes[name]=agent

    def getSubmode(self, name):
        return self.m_submodes.get(name, None)

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

    @tag('<c-f>(normal)')
    def activate(self, view=None, submode=None, **kwargs):
        super().activate()
        if not view:
            view=self.app.stateman.view()
        self.app.stateman.activate(
                view=view,
                moder=self,
                mode='hint',
                submode=submode,
                **kwargs)
        submoder=self.getSubmode(submode)
        if submoder:
            submoder.activate(view=view, **kwargs)

    @tag('<c-f>/<escape>(hint[any])')
    def octivate(self, view=None, **kwargs):
        super().octivate()
        if not view:
            view=self.app.stateman.view()
        submoder=self.app.stateman.submoder()
        if submoder:
            submoder.octivate(view=view, **kwargs)
        self.app.stateman.activate()
