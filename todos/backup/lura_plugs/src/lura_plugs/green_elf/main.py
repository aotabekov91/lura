from gizmo.plug import Plug

class GreenElf(Plug): 

    update=False

    def setup(self):

        super().setup()
        self.addColorscheme()

    def addColorscheme(self):

        styleman=self.app.styleman
        file=self.files.get(
                'colorscheme.css', None)
        if file:
            style=styleman.read(file)
            styleman.addColorscheme(
                    self.name, style, self.update)
