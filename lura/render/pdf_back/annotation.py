from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.render.base import Annotation

class PdfAnnotation(Annotation):

    def __init__(self):
        super().__init__()

    def color(self):
        return self.m_color

    def contents(self):
        return self.m_content

    def setAnnotationData(self, data):
        self.m_color=data.style().color().name()
        self.m_boundary=data.boundary().normalized()
        self.m_type=data.subType()
        self.m_content=data.contents()

    def getPosition(self):
        return '{}:{}:{}:{}'.format(
            round(self.m_boundary.x(), 8),
            round(self.m_boundary.y(), 8),
            round(self.m_boundary.width(), 8),
            round(self.m_boundary.height(), 8))

    def boundary(self):
        if hasattr(self, 'm_boundary'): return self.m_boundary
        position=self.position()
        b=[float(e) for e in position.split(':')]
        return QRectF(b[0], b[1], b[2], b[3])
