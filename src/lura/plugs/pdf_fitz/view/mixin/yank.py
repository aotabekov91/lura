from gizmo.utils import tag

class Yank:

    canYank=True

    @tag('yy', modes=['normal|^own'])
    def yankWord(self, *args, **kwargs):

        sel=self.selection()
        if sel:
            text=sel.get('text')
            if text:
                c=self.app.qapp.clipboard()
                c.setText(text)
        self.cleanUp()

    @tag('ya', modes=['normal'])
    def yankToAyleen(self, rstart=1, **kwargs):

        c=self.checkProp('hasServer', self.app)
        if not c: return
        sel=self.selection()
        if not sel: return
        text=sel.get('text')
        if not text: return
        lan='en'
        if rstart==2: lan='de'
        req={
            'target': 'Ayleen',
            'object': 'app.ui.moder.plugs.deflookup',
            'data'  : {'term':text,'lan':lan},
            'action': 'lookup',
            }
        self.cleanUp()
        return self.app.server.request(**req)
