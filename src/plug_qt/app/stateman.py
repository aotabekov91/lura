from PyQt6 import QtCore

import plug

class Stateman(
    plug.Stateman,
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

    def setMode(self, *args, **kwargs) -> str:
        super().setMode(*args, **kwargs)
        self.modeChanged.emit(self) #lookup: should it not be mode here instead of self
        return self.m_mode

    def setSubmode(self, submode: str = None, **kwargs) -> str:
        super().setSubmode(submode=submode, **kwargs)
        self.submodeChanged.emit(submode)
        return self.m_submode

    def setView(self, *args, view=None, **kwargs):
        super().setView(*args, view=view, **kwargs)
        if view:
            self.viewChanged.emit(view)

    def setSubview(self, view=None, **kwargs):
        ctype = self.m_subview
        super().setSubview(view, **kwargs)
        if ctype != self.m_subview:
            self.subviewChanged.emit(view)
