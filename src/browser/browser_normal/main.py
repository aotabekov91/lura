import functools

from plug import Plug

class BrowserNormal(Plug):

    views=['BrowserView']

    def setup(self):
        self.m_data={}
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)
        self.app.buffman.viewCreated.connect(
                self.injectJSCode)

    def isCompatible(self, view):
        if view:
            for klass in view.__class__.__mro__:
                if klass.__name__ in self.views:
                    return True
        return False

    def addAgent(self):
        holder=self.app.plugman.getPlug('Normal')
        if holder:
            holder.addAgent('goTo', 'BrowserView', self)

    def injectJSCode(self, view):
        path=self.files.get('normal.js', None)
        if self.isCompatible(view):
            self.m_data[view]={}
            view.injectJSCode(name='normal', path=path, subframes=True)

    def currentPosition(self, view=None):
        data=self.m_data.get(view, {})
        return data.get('position', {})

    def updateCurrentPosition(self, data, *, view):
        self.m_data[view]['position']=data

    def updatePositionScript(self, view): 
        script=view.scriptize('normal', 'current_position')
        functor=functools.partial(self.updateCurrentPosition, view=view)
        view.runJSCode(script, resultCallback=functor)

    def goTo(self, view=None, x=0, y=0, **kwargs):
        if view:
            script=view.scriptize('normal', 'set_current_position', x, y)
            view.runJSCode(script)

    def last(self, view=None, **kwargs):
        if view:
            size=view.page().contentsSize()
            ydelta=size.height()
            script=view.scriptize('window', 'scrollBy', 0, ydelta)
            view.page().runJavaScript(script)

    def first(self, view=None, **kwargs):
        if view:
            size=view.page().contentsSize()
            ydelta=-1*size.height()
            script=view.scriptize('window', 'scrollBy', 0, ydelta)
            view.page().runJavaScript(script)

    def right(self, view=None, xrange=[1], xdelta=100, **kwargs):
        if view:
            xdelta*=xrange[-1]
            script=view.scriptize('window', 'scrollBy', xdelta, 0)
            view.page().runJavaScript(script)

    def left(self, view=None, xrange=[1], xdelta=100, **kwargs):
        if view:
            xdelta*=-1*xrange[-1]
            script=view.scriptize('window', 'scrollBy', xdelta, 0)
            view.page().runJavaScript(script)

    def up(self, view=None, xrange=[1], ydelta=100, **kwargs):
        if view:
            ydelta*=-1*xrange[-1]
            script=view.scriptize('window', 'scrollBy', 0, ydelta)
            view.page().runJavaScript(script)

    def down(self, view=None, xrange=[1], ydelta=100, **kwargs):
        if view:
            ydelta*=xrange[-1]
            script=view.scriptize('window', 'scrollBy', 0, ydelta)
            view.page().runJavaScript(script)

    def activate(self, *args, view=None, kind=None, **kwargs):
        normal=self.app.plugman.getPlug('Normal')
        if kind and view:
            functor=getattr(self, kind, None)
            if functor:
                functor(*args, view=view, **kwargs)
                self.updatePositionScript(view)
            if normal:
                data=self.currentPosition(view)
                normal.positionChanged.emit('goTo', view, data)
