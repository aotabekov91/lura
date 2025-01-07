from plug import Plug, deleg

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
        path=self.files.get('xrange.js', None)
        if path and self.isCompatible(view):
            view.injectJSCode(name='xrange', path=path, subframes=True)

    @deleg('select@(any)[BrowserView]')
    def select(self, view, selection, **kwargs):
        if view:
            box=selection['box']
            script=view.scriptize('selection', 'select', box)
            view.runJSCode(script, **kwargs)
