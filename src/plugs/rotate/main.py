from plug import Plug, tag

class Rotate(Plug):

    def setup(self):
        super().setup()
        self.m_rotators={}

    def getRotator(self, name):
        return self.m_rotators.get(name, None)

    def addRotator(self, name, rotator):
        self.m_rotators[name]=rotator

    @tag("r(normal)")
    def rotateView(self, xrange=None):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        rotator=self.getRotator(name)
        if not rotator:
            return
        if not xrange:
            rotator.rotate(view)
        else:
            rotator.setRotation(view, xrange)

    @tag("R(normal)")
    def rotateItem(self, xrange=None):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        rotator=self.getRotator(name)
        if rotator:
            rotator.setItemRotation(view, xrange)
