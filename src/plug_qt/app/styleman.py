from PyQt6 import QtCore

import plug

class Styleman(
    plug.Styleman,
    QtCore.QObject,
):

    def setup(self) -> None:
        super().setup()
        self.setParent(self.app)
        self.app.appIsLaunched.connect(
            self.updateDefault
        )
