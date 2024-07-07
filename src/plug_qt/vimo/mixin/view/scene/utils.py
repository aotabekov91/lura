from PyQt6 import QtCore, QtWidgets


class BaseScene(QtWidgets.QGraphicsScene):
    itemAdded = QtCore.pyqtSignal(object)
    backgroundDrawn = QtCore.pyqtSignal(object, object)

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)
        self.backgroundDrawn.emit(painter, rect)

    def addItem(self, item):
        super().addItem(item)
        self.adjustScene()
        self.itemAdded.emit(item)

    def adjustScene(self):
        irect = self.itemsBoundingRect()
        irect.setX(-1000)
        irect.setY(-1000)
        irect.setWidth(irect.width() + 1000)
        irect.setHeight(irect.height() + 1000)
        self.setSceneRect(irect)
