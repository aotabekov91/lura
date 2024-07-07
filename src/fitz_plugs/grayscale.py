from plug import Plug
from plug.utils import tag

class GrayScale(Plug):

    @tag("c(normal)[FitzView]")
    def toggleGrayScale(self):
        view=self.app.stateman.view()
        for i in view.m_items.values():
            i.toggleGrayScale()
