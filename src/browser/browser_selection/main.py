from plug import Plug, deleg, tag

class BrowserSelection(Plug):

    views=['BrowserView']

    def setup(self):
        super().setup()
        self.app.buffman.viewCreated.connect(
                self.injectJSCode)

    def isCompatible(self, view):
        if view:
            for klass in view.__class__.__mro__:
                if klass.__name__ in self.views:
                    return True
        return False

    def injectJSCode(self, view):
        path=self.files.get('selection.js', None)
        if path and self.isCompatible(view):
            view.injectJSCode(name='selection', path=path, subframes=True)

    @deleg('select@(normal)[BrowserView]')
    def select(self, view, selection, **kwargs):
        if view:
            box=selection['box']
            script=view.scriptize('selection', 'select', box)
            view.runJSCode(script, **kwargs)

    @tag('!(normal)')
    def test(self):
        view=self.app.stateman.view()
        script=view.scriptize('selection', 'get_selection')
        view.runJSCode(script, resultCallback=self.n)

    def n(self, result):
        print(result)
