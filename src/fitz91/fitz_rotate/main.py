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
        holder=self.app.plugman.getPlug('Rotate')
        if holder:
            holder.addAgent('FitzView', self)
            modeller=self.app.buffman.modeller('FitzModel')
            if modeller:
                element_klass=modeller.element_class
                element_klass.addFunctor(
                        'renderMatrix', self.renderMatrix)

    def renderMatrix(self, keys, matrix):
        rotation=keys.get('rotation', False)
        if rotation:
            matrix.prerotate(rotation % 360)

    def activate(self, view=None, xrange=None, only_item=False, **kwargs):
        if view:
            item=None
            if only_item:
                item=view.currentItem()
                rotation=item.key('rotation') or 0
            else:
                rotation = self.rotation(view) or 0
            if xrange:
                rotation = (rotation + xrange[-1]) % 360
            else:
                rotation = (rotation + 90) % 360
            self.setRotation(view, rotation, item=item)

    def setRotation(self, view, rotation, item=None):
        if item:
            self.setItemRotation(item, rotation)
        else:
            for idx, item in view.getItems():
                self.setItemRotation(item, rotation)
            view.setProp('rotation', rotation)
        view.redraw()

    def setItemRotation(self, item, rotation):
        if item:
            item.setKey('rotation', rotation)
            item.redraw()

    def rotation(self, view):
        return view.getProp('rotation')
