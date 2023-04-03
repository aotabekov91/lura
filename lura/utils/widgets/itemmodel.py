from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from .item import Item

from xml.etree.ElementTree import Element, SubElement, tostring, fromstring

class ItemModel(QStandardItemModel):

    modelChanged = pyqtSignal()

    def __init__(self, m_id=None, window=None):
        super().__init__()
        self.m_id = m_id
        self.window=window
        self.m_content = ''
        self.m_collection={}
        self.setup()

    def setup(self):
        self.m_proxy=QSortFilterProxyModel()
        self.m_proxy.setSourceModel(self)
        self.m_proxy.setDynamicSortFilter(True)
        self.m_proxy.setRecursiveFilteringEnabled(True)
        self.m_proxy.setFilterCaseSensitivity(Qt.CaseInsensitive)

    def id(self):
        return self.m_id

    def setId(self, did):
        self.m_id=did

    def appendRow(self, item):
        self.invisibleRootItem().appendRow(item)

    def clear(self):
        for index in range(self.invisibleRootItem().rowCount()):
            self.invisibleRootItem().takeRow(index)

    def proxy(self):
        return self.m_proxy

    def readSuccess(self):
        return True

    def setContent(self, item=None, parentElement=None):
        if item is None:

            self.m_count = -1
            item = self.invisibleRootItem()
            element = Element('Mindmap')
            self.m_element = element

        else:

            element = SubElement(parentElement, item.kind())
            element.set('id', str(item.id()))
            element.set('p_eid', parentElement.attrib['eid'])
            if item.kind() == 'container':
                element.set('title', item.get('title'))
            if item.watchFolder() is not None:
                element.set('watch', ':'.join(item.watchFolder()))

        self.m_count += 1
        element.set('eid', str(self.m_count))

        for index in range(item.rowCount()):
            self.setContent(item.child(index), element)

    def xml(self):
        self.setContent()
        return tostring(self.m_element, encoding='unicode', method='xml')

    def update(self, *args, **kwargs):
        self.window.plugin.tables.update(
                'maps', {'id':self.m_id}, {'content':self.xml()})

    def load(self):

        if self.m_id is not None:

            items = {'0': self.invisibleRootItem()}
            mapData = self.window.plugin.tables.get(
                    'maps', {'id': self.id()})
            if mapData['content']=='': return self.connectModel()
            xml = fromstring(mapData['content'])

            for element in xml.iter():

                if element.tag == 'Mindmap': continue

                if element.attrib['p_eid'] in items:

                    kind=element.tag
                    m_id=element.attrib['id']
                    title=element.attrib.get('title', '')
                    watchFolder=element.attrib.get('watch', None)

                    item=Item(kind, m_id, self.window, title)
                    
                    if watchFolder is not None and len(watchFolder)>0:
                        pathes=watchFolder.split(':')
                        for path in pathes:
                            item.addWatchFolder(path)

                    items[element.attrib['p_eid']].appendRow(item)
                    items[element.attrib['eid']] = item

            self.connectModel()

    def connectModel(self):
        self.rowsInserted.connect(self.update)
        self.rowsRemoved.connect(self.update)
        self.rowsMoved.connect(self.update)
        self.rowsAboutToBeRemoved.connect(self.update)
        self.dataChanged.connect(self.update)

    def getAllItems(self, item=None, items=None):
        if item is None:
            item=self.invisibleRootItem()
            items=[]
        if item!=self.invisibleRootItem(): items+=[item]
        for i in range(item.rowCount()):
            self.getAllItems(item.child(i), items)
        return items
