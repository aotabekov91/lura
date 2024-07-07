from PyQt6 import QtCore


class Pixmap:
    pixmapReady = QtCore.pyqtSignal(object, object, object)
    repaintWanted = QtCore.pyqtSignal()

    def setup(self):
        super().setup()
        self.modelChanged.connect(self.connectPixmap)

    def connectPixmap(self, model):
        if model:
            model.pixmapReady.connect(self.pixmapReady)

            # model.repaintWanted.connect(
            #         self.repaintWanted)
