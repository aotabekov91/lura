from PyQt5 import QtGui, QtCore

class Normed:

    canNormalize=True

    def setup(self):

        super().setup()
        self.m_norm=QtGui.QTransform()
        self.resized.connect(self.updateNorm)

    def updateNorm(self):

        s=self.size()
        self.m_norm.reset()
        self.m_norm.scale(s.width(), s.height())

    def unify(self, p):

        norm=self.m_norm.inverted()[0]
        if type(p)==tuple:
            if len(p)==2:
                p=QtCore.QPointF(*p)
            elif len(p)==4:
                p=QtCore.QRectF(*p)
        if type(p) in [QtCore.QPoint, QtCore.QPointF]:
            u=norm.map(p)
        else:
            p=p.normalized()
            u=norm.mapRect(p)
        return u

    def unity(self, p):

        norm=self.m_norm
        if type(p)==tuple:
            if len(p)==2:
                p=QtCore.QPointF(*p)
            elif len(p)==4:
                p=QtCore.QRectF(*p)
        if type(p) in [QtCore.QPoint, QtCore.QPointF]:
            u=norm.map(p)
        else:
            p=p.normalized()
            u=norm.mapRect(p)
        return u
