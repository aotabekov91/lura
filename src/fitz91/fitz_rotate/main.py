import plug

class FitzRotate(plug.Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        normal=self.app.plugman.getPlug('Normal')
        if normal:
            normal.addAgent('rotate', 'FitzView', self)
            normal.addAgent('rotateState', 'FitzView', self)
            modeller=self.app.buffman.modeller('FitzModel')
            if modeller:
                element_klass=modeller.element_class
                element_klass.addFunctor(
                        'renderMatrix', self.renderMatrix)

    def rotateState(self, view=None, **kwargs):
        if view:
            rotation=view.getAttr('rotate', custom=True, default=0)
            return {'rotate': rotation} 
        return {}

    def renderMatrix(self, keys, matrix):
        rotate=keys.get('rotate', False)
        if rotate:
            matrix.prerotate(rotate % 360)

    def rotate(self, view=None, kind=None, xrange=[1], rotate=None, **kwargs):
        if view:
            if rotate is None:
                item=None
                if kind=='view':
                    data = self.rotateState(view=view)
                    print(data)
                    rotate=data.get('rotate', 0)
                elif kind=='item':
                    item=view.currentItem()
                    rotate=item.key('rotate') or 0
                if xrange:
                    rotate = (rotate + 90*xrange[-1]) % 360
                else:
                    rotate = (rotate + 90) % 360
            if kind=='view':
                self.rotateView(view, rotate)
            elif kind=='item' and item:
                self.rotateItem(item, rotate)
            view.redraw()
            self.reportStateChange(view)

    def reportStateChange(self, view):
        normal=self.app.plugman.getPlug('Normal')
        if normal:
            data=self.rotateState(view=view)
            normal.stateChanged.emit('rotate', view, data)

    def activate(
            self, 
            action=None, 
            view=None, 
            **kwargs):
        if action and view:
            func=getattr(self, action, None)
            if func:
                func(view=view, **kwargs)

    def rotateView(self, view, rotate):
        for idx, item in view.getItems():
            self.rotateItem(item, rotate)
        view.setAttr('rotate', rotate, custom=True)

    def rotateItem(self, item, rotate):
        item.setKey('rotate', rotate)
        item.redraw()
