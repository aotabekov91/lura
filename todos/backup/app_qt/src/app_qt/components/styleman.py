from PyQt6 import QtCore

import app

class Styleman(
    app.Styleman,
    QtCore.QObject,
):

    def setup(self) -> None:
        super().setup()
        self.setParent(self.app)
        self.app.appIsLaunched.connect(
            self.updateDefault
        )
