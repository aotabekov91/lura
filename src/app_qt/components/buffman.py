import typing as tp
from PyQt6 import QtCore

import app

class Buffman(
        app.Buffman, 
        QtCore.QObject
):

    viewCreated: QtCore.pyqtSignal = QtCore.pyqtSignal(
        object
    )
    modelCreated: QtCore.pyqtSignal = QtCore.pyqtSignal(
        object
    )
    viewAdded = QtCore.pyqtSignal(object)
    viewClosed = QtCore.pyqtSignal(object)
    posIndexChanged = QtCore.pyqtSignal(
        object, object, object
    )

    typerAdded = QtCore.pyqtSignal(object)
    viewerAdded = QtCore.pyqtSignal(object)
    modelLoaded = QtCore.pyqtSignal(object)
    modellerAdded = QtCore.pyqtSignal(object)

    def setup(self) -> None:
        super().setup()
        self.setParent(self.app)
        self.app.appIsLaunched.connect(self.checkParser)

    def setModel(self, idx: tp.Any, model: tp.Any) -> None:
        super().setModel(idx, model)
        if model:
            self.modelCreated.emit(model)

    def saveView(self, model: tp.Any, view: tp.Any) -> None:
        super().saveView(model, view)
        if view:
            self.viewCreated.emit(view)

    def create(self, klass, **kwargs):
        view = super().create(klass, **kwargs)
        self.viewCreated.emit(view)
        return view

    def addView(self, view):
        signal = view.getAttr("posIndexChanged", "signal")
        if signal:
            signal.connect(self.posIndexChanged)
        self.viewAdded.emit(view)

    def locate(self, view, **kwargs):
        man = super().locate(view, **kwargs)
        if man:
            man.addView(view, **kwargs)
        return man

    def addViewer(self, klass: tp.Any) -> tp.Any:
        cond = not klass in self.m_viewers
        super().addViewer(klass)
        if cond:
            self.viewerAdded.emit(klass)
        return klass

    def addModeller(self, klass: tp.Any) -> tp.Any:
        cond = not klass in self.m_modellers
        super().addModeller(klass)
        if cond:
            self.modellerAdded.emit(klass)
        return klass

    def createModel(self, *args, **kwargs):
        model = super().createModel(*args, **kwargs)
        if model:
            self.modelCreated.emit(model)
        return model
