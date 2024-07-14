from plug import Plug, tag
from plug_qt.vimo.mixin import view

class CopyFitzView(view.Copy):

    canCopy=True

    def copy(self, *args, **kwargs):
        pos = self.getPosition()
        mode = self.scaleMode
        copy = super().copy(*args, **kwargs)
        copy.goTo(*pos)
        copy.setScaleMode(mode)
        return copy

class FitzCopy(Plug):

    def setup(self):
        super().setup()
        self.app.appSoonStarts.connect(
                self.updateFitz)

    def updateFitz(self):
        self.app.wait()
        viewers=self.app.buffman.viewers()
        for name, klass in viewers.items(): 
            if name=='FitzView':
                self.updateFitzViewer(klass)
                break
        self.app.wait(-1)

    def updateFitzViewer(self, viewer):
        name=viewer.__name__
        mro=(CopyFitzView, viewer)
        viewer=type(name, mro, {})
        self.app.buffman.addViewer(name, viewer)

