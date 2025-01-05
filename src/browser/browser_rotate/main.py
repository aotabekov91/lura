import plug
import functools

class BrowserRotate(plug.Plug):

    def setup(self):
        super().setup()
        self.addAgent()

    def addAgent(self):
        self.app.delegman.addAgent(
                'normal', None, 'BrowserView', 'rotate', self.rotate)
        self.app.delegman.addAgent(
                'normal', None, 'BrowserView', 'rotateState', self.rotateState)

    def rotate(self, view=None, kind=None, xrange=[1], rotate=None, **kwargs):
        if view:
            if rotate is None:
                item=None
                if kind=='view':
                    data = self.rotateState(view=view)
                    rotate=data.get('rotate', 0)
                elif kind=='item':
                    item=view.currentItem()
                    rotate=item.key('rotate') or 0
                if xrange:
                    rotate = (rotate + 90*xrange[-1]) % 360
                else:
                    rotate = (rotate + 90) % 360
            if kind=='view':
                self.rotateView(view, rotate, **kwargs)
            elif kind=='item' and item:
                self.rotateItem(item, rotate, **kwargs)
            view.redraw()
            self.reportStateChange(view)

    def rotateState(self, view=None, **kwargs):
        if view:
            rotation=view.getAttr('rotate', custom=True, default=0)
            return {'rotate': rotation} 
        return {}

    def reportStateChange(self, view):
        normal=self.app.plugman.getPlug('Normal')
        if normal:
            data=self.rotateState(view=view)
            normal.stateChanged.emit('rotate', view, data)

    def updateRotate(self, result, *, view, rotate):
        view.setAttr('rotate', rotate, custom=True)

    def rotateView(self, view, rotate, **kwargs):
        script=f"document.body.style.setProperty('-webkit-transform', 'rotate({rotate}deg)', null);"
        functor=functools.partial(self.updateRotate, view=view, rotate=rotate)
        view.runJSCode(script, resultCallback=functor)

    def rotateItem(self, item, rotate, **kwargs):
        # todo: rotate invididual elements, e.g., images
        pass
