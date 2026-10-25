from plug import Plug, deleg

class FitzGrayscale(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addToGrayscaler()
        else:
            self.app.appSoonStarts.connect(
                    self.addToGrayscaler)

    def addToGrayscaler(self):
        modeller=self.app.buffman.modeller('FitzModel')
        if modeller:
            element_klass=modeller.element_class
            element_klass.addFunctor(
                    'renderImage', self.renderImage)

    def renderImage(self, keys, img):
        gray_scale=keys.get('grayscale', False)
        if gray_scale:
            img.invertPixels()
        return img

    @deleg('toggleGrayscale@(normal)[FitzView]')
    def toggleGrayscale(self, view=None, **kwargs):
        if view:
            grayscale=view.checkProp('grayscale')
            view.setProp('grayscale', not grayscale)
            grayscale=view.checkProp('grayscale')
            for item in view.m_items.values():
                item.setKey('grayscale', grayscale)
            view.redraw()
