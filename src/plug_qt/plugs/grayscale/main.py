from plug import Plug, tag

class Grayscale(Plug):

    prefix_keys=["<c-w>(normal)"]

    @tag("C(normal)")
    def toggleGrayScale(self, view=None, **kwargs):
        view=view or self.app.stateman.view()
        self.app.delegman.delegate(
                mode='normal',
                view=view,
                data=kwargs,
                action='toggleGrayscale')
