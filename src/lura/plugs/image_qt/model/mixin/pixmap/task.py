from PyQt5 import QtCore, QtGui

class Task(QtCore.QObject):

    pixmapReady = QtCore.pyqtSignal(
            object, object, object)

    def __init__(self, model, queue):

        self.m_model=model
        self.m_queue=queue
        super().__init__()

    def run(self):

        self.running=True
        while self.running:
            i, d = self.m_queue.get()
            data=self.m_model.loadData(i)
            img = self.renderImage(*d, img_data=data)
            if img:
                p=QtGui.QPixmap.fromImage(img)
                self.pixmapReady.emit(i, d, p)

    def renderImage(
            self, 
            idx, 
            x, 
            y, 
            scale,
            rotation, 
            pratio,
            grayScale,
            clip,
            trim,
            img_data,
            ):

        d=img_data.get('img')
        s=img_data.get('size')
        if d:
            w=int(s.width()*x)
            h=int(s.height()*y)
            img=d.scaled(
                    w, h, QtCore.Qt.KeepAspectRatio)
            if grayScale: img.invertPixels()
            return img
