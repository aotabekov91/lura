from gizmo.utils import tag

class Yank:

    canYank=True

    @tag('yy', modes=['normal|^own'])
    def yankWord(self):

        sel=self.selection()
        if sel:
            text=sel.get('text')
            if text:
                c=self.app.qapp.clipboard()
                c.setText(text)
        self.cleanUp()
