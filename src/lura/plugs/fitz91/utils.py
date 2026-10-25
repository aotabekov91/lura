from PyQt6 import QtCore, QtGui, QtWidgets

class Task(QtCore.QObject):

    pixmapReady = QtCore.pyqtSignal(object, object, object)

    def __init__(self, queue):
        self.m_queue = queue
        super().__init__()

    def run(self):
        self.running = True
        while self.running:
            element, key = self.m_queue.get()
            img = element.renderImage(key)
            pixmap = QtGui.QPixmap.fromImage(img)
            self.pixmapReady.emit(element, key, pixmap)

class Viewport(QtWidgets.QWidget):

    updated = QtCore.pyqtSignal()

    def update(self, *args, **kwargs):
        super().update(*args, **kwargs)
        self.updated.emit()

    def event(self, event):
        result = super().event(event)
        if event.type() == QtCore.QEvent.Type.Move:
            self.update()
        return result

class FitzScene(QtWidgets.QGraphicsScene):

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
