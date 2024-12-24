from plug import Plug, tag

class Grayscale(Plug):

    def setup(self):
        super().setup()
        self.m_grayscalers={}

    def getGrayscaler(self, name):
        return self.m_grayscalers.get(name, None)

    def addGrayscaler(self, name, grayscaler):
        self.m_grayscalers[name]=grayscaler

    @tag("c(normal)")
    def toggleGrayScale(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        grayscaler=self.getGrayscaler(name)
        if grayscaler:
            grayscaler.toggleGrayscale(view)
