from plug import Plug

class FitzQuickmark(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addToQuickmarker()
        else:
            self.app.appSoonStarts.connect(
                    self.addToQuickmarker)

    def addToQuickmarker(self):
        quickmarker=self.app.plugman.plugs.get(
                'Quickmark')
        if quickmarker:
            quickmarker.addQuickmarker(
                    'FitzView', self)

    def quickmark(self, quickmark, view):
        data = {"quickmark": quickmark}
        data = view.getLocator(data=data, kind="uniq")
        return view.getLocator(data=data, kind="position")

    def go(self, data, view):
        view.openLocator(data, kind="position")
