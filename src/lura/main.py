import faulthandler
faulthandler.enable()

from plug_qt import App

from lura.plugs import get_base_plugs

class Lura(App):

    def activate(self, *args, **kwargs):
        super().activate(*args, **kwargs)
        self.plugman.loadKlasses(get_base_plugs())

def run():
    app = Lura()
    app.activate()
    app.run()
