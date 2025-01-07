from plug import Plug, deleg

class FitzRotate(Plug):

    def setup(self):
        super().setup()
        if self.app.running: 
            self.updateFitzModel()
        else:
            self.app.appSoonStarts.connect(
                    self.updateFitzModel)

    def updateFitzModel(self):
        modeller=self.app.buffman.modeller('FitzModel')
        if modeller:
            element_klass=modeller.element_class
            element_klass.addFunctor(
                    'renderMatrix', self.renderMatrix)

    def renderMatrix(self, keys, matrix):
        rotate=keys.get('rotate', False)
        if rotate:
            matrix.prerotate(rotate % 360)

    @deleg('rotateState@(normal)[FitzView]')
    def rotateState(self, view=None, **kwargs):
        if view:
            rotation=view.getAttr('rotate', custom=True, default=0)
            return {'rotate': rotation} 
        return {}

    @deleg('rotate@(normal)[FitzView]')
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

    def rotateView(self, view, rotate):
        for idx, item in view.getItems():
            self.rotateItem(item, rotate)
        view.setAttr('rotate', rotate, custom=True)

    def rotateItem(self, item, rotate):
        item.setKey('rotate', rotate)
        item.redraw()
