from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from .base import BaseMapDocument

from lura.core.widgets.tree import Item
from lura.core.widgets.tree import Container

from xml.etree.ElementTree import Element, SubElement, Comment, tostring, fromstring

class MapDocument(BaseMapDocument):

    rowsInserted = pyqtSignal('QModelIndex', int, int)
    rowsRemoved = pyqtSignal('QModelIndex', int, int)
    rowsMoved = pyqtSignal('QModelIndex', int, int)
    rowsAboutToBeRemoved = pyqtSignal('QModelIndex', int, int)
    dataChanged = pyqtSignal('QModelIndex')
    modelChanged = pyqtSignal()

    annotationAdded=pyqtSignal(object)

    def __init__(self, m_id=None):
        super().__init__()
        self.m_id = m_id
        self.m_title = 'Mindmap'
        self.m_content = ''
        self.m_block=False
        self.m_collection={}

    def isOnline(self):
        return False

    def readSuccess(self):
        return True

    def title(self):
        return self.m_db.title(self)

    def setTitle(self, title):
        self.m_db.setTitle(self, title)

    def setContent(self, item=None, parentElement=None):
        if item is None:

            self.m_count = -1
            item = self.m_model.invisibleRootItem()
            element = Element('Mindmap')
            self.m_element = element

        else:

            element = SubElement(parentElement, item.kind())
            element.set('id', str(item.id()))
            element.set('p_eid', parentElement.attrib['eid'])
            if item.kind() == 'container':
                element.set('title', item.get('title'))

        self.m_count += 1
        element.set('eid', str(self.m_count))

        for index in range(item.rowCount()):
            self.setContent(item.child(index), element)

    def xml(self):
        self.setContent()
        return tostring(self.m_element, encoding='unicode', method='xml')

    def setBlock(self, condition):
        self.m_block=condition

    def update(self, *args, **kwargs):
        if not self.m_block: self.m_db.setContent(self, self.xml())

    def element(self):
        return self.m_element

    def setElement(self, element):
        self.m_element = element

    def setDB(self, db):
        self.m_db = db
        self.load()

    def db(self):
        return self.m_db

    def load(self):

        if self.m_id is not None:

            self.m_model = QStandardItemModel()

            items = {'0': self.m_model.invisibleRootItem()}
            mapData = self.m_db.get(self.id())
            if mapData['content']=='': return self.connectModel()
            xml = fromstring(mapData['content'])

            for element in xml.iter():

                if element.tag == 'Mindmap': continue

                if element.attrib['p_eid'] in items:
                    kind=element.tag
                    m_id=element.attrib['id']
                    title=element.attrib.get('title', '')
                    item=Item(kind, m_id, self.parent(), title)
                    items[element.attrib['p_eid']].appendRow(item)
                    items[element.attrib['eid']] = item
                    time=getattr(element.attrib, 'createTime', None)
                    if time is not None: item.setCreateTime(float(time))

            self.connectModel()

    def connectModel(self):
        super().connectModel()
        self.rowsInserted.connect(self.update)
        self.rowsRemoved.connect(self.update)
        self.rowsMoved.connect(self.update)
        self.rowsAboutToBeRemoved.connect(self.update)
        self.dataChanged.connect(self.update)

    def disconnectModel(self):
        self.rowsInserted.disconnect(self.update)
        self.rowsRemoved.disconnect(self.update)
        self.rowsMoved.disconnect(self.update)
        self.rowsAboutToBeRemoved.disconnect(self.update)
        self.dataChanged.disconnect(self.update)
