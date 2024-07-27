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

