from .container import Container

class Data:
    def __init__(self, element, plugins):
        self.m_element=element
        self.m_id=int(element.attrib['id'])
        self.plugins=plugins

        if element.tag == 'document':
            self.m_plugin = plugins.tables.metadata
            self.row_id_name='did'
        elif element.tag == 'note':
            self.m_plugin = plugins.tables.notes
            self.row_id_name='id'
        elif element.tag == 'annotation':
            self.m_plugin = plugins.tables.annotations
            self.row_id_name='id'
        elif element.tag == 'container':
            self.m_plugin = Container(element.attrib['title'])
            self.row_id_name='id'

    def getField(self, fieldName):
        if fieldName=='filePath':
            return self.plugins.documents.filePath(self.m_id)
        elif fieldName=='kind':
            return self.m_element.tag
        else:
            return self.m_plugin.getField(fieldName, self.row_id_name, self.m_id)
