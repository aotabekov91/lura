from PyQt5 import QtCore

class Annotation(QtCore.QObject):

    def __init__(self, annotationData):

        super().__init__()
        self.m_data = annotationData
        self.m_aData={'data': annotationData}

    def id(self): 
        return self.m_aData.get('id', None)

    def setId(self, m_id): 

        self.m_id=m_id
        self.m_aData['id']=m_id

    def page(self): 
        return self.m_page

    def setPage(self, page): 
        self.m_page=page

    def color(self): 
        return self.m_aData['data'].style().color().name()

    def type(self): 
        return self.m_aData['data'].subType()

    def data(self): 
        return self.m_aData['data']

    def aData(self): 
        return self.m_aData

    def setAData(self, data): 
        self.m_aData=data

    def boundary(self): 
        return self.m_aData['data'].boundary()

    def position(self):

        topLeft=self.m_data.highlightQuads()[0].points[0]
        bottomRight=self.m_data.highlightQuads()[0].points[2]
        x, y=topLeft.x(), topLeft.y()
        x_, y_=bottomRight.x(), bottomRight.y()

        first_line=':'.join(str(round(f, 5)) for f in [x, y, x_, y_])

        topLeft=self.m_data.highlightQuads()[-1].points[0]
        bottomRight=self.m_data.highlightQuads()[-1].points[2]
        x, y=topLeft.x(), topLeft.y()
        x_, y_=bottomRight.x(), bottomRight.y()

        last_line=':'.join(str(round(f, 5)) for f in [x, y, x_, y_])

        return f'{first_line}_{last_line}'

    def contains(self, point):

        for quad in self.m_data.highlightQuads():
            points=quad.points
            rectF=QtCore.QRectF()
            rectF.setTopLeft(points[0])
            rectF.setTopRight(points[1])
            rectF.setBottomRight(points[2])
            rectF.setBottomLeft(points[3])
            if rectF.contains(point): 
                return True
        return False

    def contents(self): 
        return self.m_data.contents()

    def setColor(self, color):

        style.setColor(color)
        self.m_data.setStyle(style)
