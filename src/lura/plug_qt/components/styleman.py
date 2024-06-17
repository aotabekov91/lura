from PyQt6 import QtCore

from lura.gizmo import ui


class Styleman(
    ui.core.components.Styleman,
    QtCore.QObject,
):
    def setup(self) -> None:
        super().setup()
        self.setParent(self.app)
        self.app.plugman.plugsLoaded.connect(
            self.updateDefault
        )
