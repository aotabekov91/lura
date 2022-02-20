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

    def kind(self):
        return 'annotation'

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
        if hasattr(self, 'm_color'): self.setColor(self.m_color)
        if hasattr(self, 'm_boundary'): self.setPosition(self.getPosition())

    def quote(self):
        return self.m_db.quote(self)

    def setQuote(self, quote):
        self.m_db.setQuote(self, quote)
        self.wasModified.emit(self)

    def title(self):
        return self.m_db.title(self)

    def page(self):
        return self.m_page

    def color(self):
        return QColor(self.m_db.color(self))

    def content(self):
        return self.m_db.content(self)

    def getQuote(self):
        return ''

    def data(self):
        return self.m_db.data(self)

    def setPage(self, page):
        self.m_page=page

    def setTitle(self, title):
        self.m_db.setTitle(self, title)
        self.wasModified.emit(self)

    def setColor(self, color):
        self.m_db.setColor(self, color)
        self.wasModified.emit(self)

    def setContent(self, content):
        self.m_db.setContent(self, content)
        self.wasModified.emit(self)

    def getKind(self):
        self.m_db.getKind(self)

    def position(self):
        return self.m_db.position(self)

    def setPosition(self, position):
        self.m_db.setPosition(self, position)

    def getPosition(self):
        return self.m_data.getPosition()

    def boundary(self):
        return self.m_data.boundary()

    def setBoundary(self, boundary):
        self.m_boundary=boundary
