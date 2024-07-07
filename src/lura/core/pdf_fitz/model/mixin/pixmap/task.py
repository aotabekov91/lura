from PyQt6 import QtCore, QtGui


class Task(QtCore.QObject):
    pixmapReady = QtCore.pyqtSignal(object, object, object)

    def __init__(self, model, queue):
        self.m_model = model
        self.m_queue = queue
        super().__init__()

    def run(self):
        self.running = True
        while self.running:
            i, d = self.m_queue.get()
            e = self.m_model.element(i)
            img = e.renderImage(**d)
            p = QtGui.QPixmap.fromImage(img)
            self.pixmapReady.emit(i, d, p)
