import typing as tp
from PyQt6 import QtCore

import plug

class Plugman(
        plug.Plugman, 
        QtCore.QObject,
):

    plugAdded = QtCore.pyqtSignal(object)
    modeAdded = QtCore.pyqtSignal(object)
    plugsLoaded = QtCore.pyqtSignal(object)
    actionsRegistered = QtCore.pyqtSignal(object, object)

    def setup(self):
        super().setup()
        self.setParent(self.app)

    def load(self, *args, **kwargs) -> tp.Set[tp.Any]:
        super().load(*args, **kwargs)
        # todo: maybe only loaded plugs
        return self.plugsLoaded.emit(self.plugs)

    def add(self, plug):
        super().add(plug)
        if hasattr(plug, "actions"):
            self.save(plug, plug.actions)
        self.plugAdded.emit(plug)
        if hasattr(plug, "isMode"):
            self.modeAdded.emit(plug)

    def save(self, plug, actions):
        super().save(plug, actions)
        self.actionsRegistered.emit(plug, actions)
