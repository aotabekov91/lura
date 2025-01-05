import functools

from plug import Plug

class BrowserNormal(Plug):

    views=['BrowserView']

    def setup(self):
        super().setup()
        self.m_states={}
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
        self.app.delegman.addAgent(
                'normal', None, 'goTo', 'BrowserView', self.goTo)
        self.app.delegman.addAgent(
                'normal', None, 'goToState', 'BrowserView', self.goToState)

    def delegate(self, action=None, **kwargs):
        if action:
            func = getattr(self, action, None)
            if func:
                return func(**kwargs)

    def goTo(
            self, 
            kind=None, 
            view=None, 
            xrange=[1], 
            x=None, 
            y=None, 
            id=None,
            xdelta=100, 
            ydelta=100, 
            **kwargs):
        if view:
            page=view.page()
            size=page.contentsSize()
            if kind=='last':
                ydelta=size.height()
                script=view.scriptize('window', 'scrollBy', 0, ydelta)
                page.runJavaScript(script)
            elif kind=='first':
                ydelta=-1*size.height()
                script=view.scriptize('window', 'scrollBy', 0, ydelta)
                page.runJavaScript(script)
            elif kind=='right':
                xdelta*=xrange[-1]
                script=view.scriptize('window', 'scrollBy', xdelta, 0)
                page.runJavaScript(script)
            elif kind=='left':
                xdelta*=-1*xrange[-1]
                script=view.scriptize('window', 'scrollBy', xdelta, 0)
                page.runJavaScript(script)
            elif kind=='up':
                ydelta*=-1*xrange[-1]
                script=view.scriptize('window', 'scrollBy', 0, ydelta)
                page.runJavaScript(script)
            elif kind=='down':
                ydelta*=xrange[-1]
                script=view.scriptize('window', 'scrollBy', 0, ydelta)
                page.runJavaScript(script)
            elif not None in [x, y]:
                self.goToXrange(view=view, x=x, y=y, **kwargs)
            elif id is not None:
                self.goToId(view=view, id=id, **kwargs)
            self.updatePositionScript(view)

    def goToId(self, view=None, id=None, **kwargs):
        if view:
            script=view.scriptize('goTo', 'go_to_id', id)
            view.runJSCode(script)

    def goToXrange(self, view=None, x=0, y=0, **kwargs):
        if view:
            script=view.scriptize('goTo', 'set_current_position', x, y)
            view.runJSCode(script)

    def goToState(self, view=None, **kwargs):
        data=self.m_states.get(view, {})
        return data.get('position', {})

    def injectJSCode(self, view):
        path=self.files.get('goto.js', None)
        if self.isCompatible(view):
            self.m_states[view]={}
            view.injectJSCode(name='goTo', path=path, subframes=True)

    def updatePositionScript(self, view): 
        script=view.scriptize('goTo', 'current_position')
        functor=functools.partial(self.updateCurrentPosition, view=view)
        view.runJSCode(script, resultCallback=functor)

    def updateCurrentPosition(self, data, *, view):
        self.m_states[view]['position']=data
        self.reportStateChange(view)

    def reportStateChange(self, view):
        data=self.goToState(view)
        normal=self.app.plugman.getPlug('Normal')
        if normal and data:
            normal.stateChanged.emit('goTo', view, data)
