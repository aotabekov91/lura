import plug

class FitzRotate(plug.Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addToRotator()
        else:
            self.app.appSoonStarts.connect(
                    self.addToRotator)

    def addToRotator(self):
        rotator=self.app.plugman.getPlug('Rotate')
        if not rotator:
            return
        rotator.addRotator('FitzView', self)
        modeller=self.app.buffman.modeller('FitzModel')
        if not modeller:
            return
        element_klass=modeller.element_class
        element_klass.addFunctor(
                'renderMatrix', self.renderMatrix)

    def renderMatrix(self, keys, matrix):
        rotation=keys.get('rotation', False)
        if not rotation:
            matrix.prerotate(rotation % 360)
        return matrix

    def setRotation(self, view, xrange):
        rotation=0
        if xrange:
            rotation=xrange[-1]
        for item in view.items():
            item.setKey('rotation', rotation)
            # todo: problem with view items
            # only loaded items are being rotated
            # maybe: load all items in view without rendering them
        view.setProp('rotation', rotation)
        view.redraw()

    def setItemRotation(self, view, rotation):
        item = view.currentItem()
        if item:
            item.setKey('rotation', rotation)
        view.redraw()

    def rotation(self, view):
        return view.getProp('rotation')

    def rotate(self, view, by=90):
        rotation = self.rotation(view) or 0
        rotation = (rotation + by) % 360
        self.setRotation(view, [rotation])
