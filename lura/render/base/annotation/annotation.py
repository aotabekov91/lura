from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from lura.core.widgets import AnnotationProxyWidget
from lura.core.widgets.tree import AnnotationTreeWidget

class Annotation(QObject):

    wasModified = pyqtSignal(object)
    toBeRemoved=pyqtSignal(object)
    registered=pyqtSignal()

    def __init__(self):
        super().__init__()
        self.m_id=None

    def setAnnotationData(self, data):
        self.m_color=data.style().color().name()
        self.m_boundary=data.boundary()

    def widget(self):
        return AnnotationTreeWidget(self)

    def proxyWidget(self):
        return AnnotationProxyWidget(self)

    def __eq__(self, other):
        return self.id()==other.id()

    def __hash__(self):
        return self.id()

    def leftTop(self):
        pos=self.position().split(':')
        point=QPointF(float(pos[0]), float(pos[1]))
        # mappedPoint=self.page().pageItem().mapToItem(point)[1]
        return point.x(), point.y()

    def setDB(self, db):
        self.m_db=db

    def setTagDB(self, db):
        self.tagDB=db

    def tags(self):
        return self.tagDB.elementTags(self)

    def setTags(self, tags):
        self.tagDB.setElementTags(self, tags)
        self.registered.emit()

    def db(self):
        return self.m_db

    def id(self):
        return self.m_id

    def setId(self, aid):
        self.m_id=aid
        if hasattr(self, 'm_color'): self.setField('color', self.m_color)
        if hasattr(self, 'm_boundary'): self.setField('position', self.getPosition())

    def page(self):
        return self.m_page

    def getQuote(self):
        return ''

    def data(self):
        return self.m_db.data(self)

    def setPage(self, page):
        self.m_page=page

    def getPosition(self):
        return self.m_data.getPosition()

    def setBoundary(self, boundary):
        self.m_boundary=boundary

    def getField(self, fieldName):
        if fieldName=='kind':
            return 'annotation'
        elif fieldName=='color':
            return QColor(self.m_db.getField(
                        fieldName, row_id_name='did', row_id_value=self.m_id))
        return self.m_db.getField(fieldName, row_id_name='did', row_id_value=self.m_id)

    def setField(self, fieldName, fieldValue):
        self.m_db.setField(fieldName, fieldValue, row_id_name='did', row_id_value=self.m_id)
