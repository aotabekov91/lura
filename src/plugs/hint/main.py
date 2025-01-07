from plug import Plug, tag, deleg

class Hint(Plug):

    alpha: str = "abcdefghijklmnopqrstuvwxyz"

    @deleg('generateHints@(hint])')
    def generateHints(self, alist=[], kind="letters", **kwargs):
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
            if kind == "letters":
                hint = mapToLetters(num, number)
            else:
                hint = str(num + 1)
            hints[hint]=data
        return number, hints

    @deleg('hint@(normal)')
    @tag('<c-f>(normal)')
    def activate(self, view=None, submode=None, **kwargs):
        super().activate()
        if not view:
            view=self.app.stateman.view()
        self.app.stateman.activate(
                moder=self,
                mode='hint',
                submode=submode,
                **kwargs)
        data=kwargs.copy()
        data['view']=view
        self.app.delegman.delegate(
                mode='hint', 
                submode=submode, 
                action='activate',
                data=data)

    @deleg('normal@(hint)')
    @tag('<c-f>/<escape>(hint)')
    def octivate(self, view=None, submode=None, **kwargs):
        super().octivate()
        if not view:
            view=self.app.stateman.view()
        if not submode:
            submode=self.app.stateman.submode()
        data=kwargs.copy()
        data['view']=view
        self.app.delegman.delegate(
                mode='hint', 
                submode=submode, 
                action='octivate',
                data=data)
        self.app.stateman.activate()
