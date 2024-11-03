from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class Scene(QGraphicsScene):

    itemAdded=pyqtSignal(object)
    backgroundDrawn=pyqtSignal(object, object)

    def drawBackground(self, painter, rect):

        super().drawBackground(painter, rect)
        self.backgroundDrawn.emit(painter, rect)

    def addItem(self, item):

        super().addItem(item)
        self.adjustScene()
        self.itemAdded.emit(item)

    def adjustScene(self):

        irect=self.itemsBoundingRect()
        irect.setX(-1000)
        irect.setY(-1000)
        irect.setWidth(irect.width()+1000)
        irect.setHeight(irect.height()+1000)
        self.setSceneRect(irect)
