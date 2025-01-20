from plug import Plug

class BrowserCaret(Plug):

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
        path=self.files.get('caret.js', None)
        if path and self.isCompatible(view):
            view.injectJSCode(name='caret', path=path, subframes=True)
