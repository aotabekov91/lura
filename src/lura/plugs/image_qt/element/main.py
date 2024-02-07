import gizmo
from PyQt5 import QtCore, QtGui

class ImageQtElement(
        gizmo.vimo.element.Element, 
        QtCore.QObject
        ):

    dataChanged=QtCore.pyqtSignal()

    def setup(self):

        super().setup()
        self.m_path=None
        self.m_size=QtCore.QSizeF()
        self.m_norm= QtGui.QTransform()

    def updateTrans(self):

        n=self.m_norm
        s=self.size()
        n.scale(s.width(), s.height())
        ninv=n.inverted()[0]
        self.m_norm_inv=ninv

    def setData(self, data=None, index=None):

        if self.m_index!=index:
            self.m_index=index
            self.m_path=data.get('path')
            self.m_size=data.get('size')
            self.m_identifier=data.get('idx')
            self.m_data=data.get('img')
            self.updateTrans()
            self.dataChanged.emit()

    def path(self):
        return self.m_path

    def size(self):
        return self.m_size

    def setSize(self, size):
        self.m_size=size

    def resetIndex(self, idx):

        d=self.m_model.loadData(idx)
        if d: self.setData(data=d, index=idx)

    def render(self, data, **kwargs):

        return self.m_model.getPixmapCache(
                self.index(), data)
