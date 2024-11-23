from plug import Plug, tag

class Hint(Plug):

    alpha: str = "abcdefghijklmnopqrstuvwxyz"

    def setup(self):
        super().setup()
        self.m_hinters={}

    def addHinter(self, name, hinter):
        self.m_hinters[name]=hinter

    def hinter(self, name):
        return self.m_hinters.get(name, None)

    @tag(["<c-f>(normal)", "<c-f>/<c-[>(hint)"])
    def toggleHint(self):
        self.app.stateman.toggle(
                mode="hint", delisten=True)

    @tag("<escape>(hint[any])")
    def finishHintMode(self):
        self.app.stateman.toggle()

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
