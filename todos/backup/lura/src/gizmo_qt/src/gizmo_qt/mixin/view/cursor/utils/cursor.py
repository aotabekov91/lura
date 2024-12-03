from PyQt6.QtCore import QObject


class BaseCursor(QObject):
    def __init__(self, view, config={}):
        self.m_config = config
        super().__init__(view)
        view.itemMouseMoveOccured.connect(self.on_mouseMove)
        view.itemMousePressOccured.connect(
            self.on_mousePress
        )
        view.itemMouseReleaseOccured.connect(
            self.on_mouseRelease
        )
        view.itemMouseDoubleClickOccured.connect(
            self.on_doubleClick
        )
        self.setSettings()
        self.setup()

    def setSettings(self):
        c = self.m_config
        for k, v in c.items():
            setattr(self, k, v)

    def setup(self):
        pass

    def on_mouseMove(self, view, item, event):
        pass

    def on_mouseRelease(self, view, item, event):
        pass

    def on_mousePress(self, view, item, event):
        pass

    def on_doubleClick(self, view, item, event):
        pass
