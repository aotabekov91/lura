from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class PdfAnnotation(QObject):

    def __init__(self, annotationData):
        super().__init__()
        self.m_data = annotationData

    def id(self):
        return self.m_id

    def setId(self, m_id):
        self.m_id=m_id

    def page(self):
        return self.m_page

    def setPage(self, page):
        self.m_page=page

    def color(self):
        return self.m_data.style().color().name()

    def type(self):
        return self.m_data.subType()

    def data(self):
        return self.m_data

    def setData(self, data):
        self.m_data=data

    def boundary(self):
        return self.m_data.boundary()

    def position(self):

        # # new positon format to annotate from db into pdf file
        # q=[]
        # for quad in self.m_data.highlightQuads():
        #     p=quad.points
        #     q+=['{}:{}:{}:{}'.format(
        #         round(p[0], 8), round(p[1], 8), round(p[2], 8), round(p[3], 8))]
        # r='_'.join(q)

        return '{}:{}:{}:{}'.format(
            round(self.boundary().x(), 8),
            round(self.boundary().y(), 8),
            round(self.boundary().width(), 8),
            round(self.boundary().height(), 8))

    def contains(self, point):
        for quad in self.m_data.highlightQuads():
            points=quad.points
            rectF=QRectF()
            rectF.setTopLeft(points[0])
            rectF.setTopRight(points[1])
            rectF.setBottomRight(points[2])
            rectF.setBottomLeft(points[3])
            if rectF.contains(point): return True
        return False

    def setColor(self, color):
        style.setColor(color)
        self.m_data.setStyle(style)
