from PyQt6 import QtCore

import plug

class Plugman(
        plug.Plugman, 
        QtCore.QObject,
):

    plugsLoaded = QtCore.pyqtSignal(object)

    def setup(self):
        super().setup()
        self.setParent(self.app)

    def loadPlugs(self, *args, **kwargs):
        super().loadPlugs(*args, **kwargs)
        return self.plugsLoaded.emit(self.plugs)
