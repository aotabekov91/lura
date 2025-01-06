from plug import Plug, tag

class BrowserAnnotate(Plug):

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
        path=self.files.get('annotate.js', None)
        if path and self.isCompatible(view):
            view.injectJSCode(name='annotate', path=path, subframes=True)

    def activate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        if view:
            script=view.scriptize('elements', 'get_selection')
            view.runJSCode(script, resultCallback=self.test)
            script="alert(navigator.userAgent)"
            view.runJSCode(script, resultCallback=self.test)

    def test(self, selection):
        print(selection)
