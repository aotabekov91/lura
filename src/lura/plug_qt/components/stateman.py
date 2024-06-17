from PyQt6 import QtCore

from lura.gizmo import ui

class Stateman(
    ui.core.components.Stateman,
    QtCore.QObject,
):
    viewChanged = QtCore.pyqtSignal(object)
    modeChanged = QtCore.pyqtSignal(object)
    subviewChanged = QtCore.pyqtSignal(object)
    submodeChanged = QtCore.pyqtSignal(object)

    def setup(self):
        super().setup()
        self.app.appIsLaunched.connect(
            self.setViewDefaultMode
        )

    def setMode(self, mode: str) -> str:
        super().setMode(mode)
        self.modeChanged.emit(self)
        return self.m_mode

    def setSubmode(
        self, submode: str = None, **kwargs
    ) -> str:
        super().setSubmode(submode, **kwargs)
        self.submodeChanged.emit(submode)
        return self.m_submode

    def setView(
            self, 
            *args, 
            view=None,
            **kwargs):
        super().setView(
                *args, view=view, **kwargs)
        if view:
            self.viewChanged.emit(view)

    def setSubview(self, view=None):
        ctype = self.m_subview
        super().setSubview(view)
        if ctype != self.m_subview:
            self.subviewChanged.emit(view)
