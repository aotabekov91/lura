class Page:

    def __init__(self, page):
        self.m_data = page

    def setPageItem(self, pageItem):
        self.m_pageItem=pageItem

    def pageItem(self):
        return self.m_pageItem

    def pageNumber(self):
        return self.m_pageNumber

    def setPageNumber(self, pageNumber):
        self.m_pageNumber=pageNumber

    def __hash__(self):
        return hash(self.m_data.data())

    def __eq__(self, other):
        return hash(self.m_data.data())==hash(other.m_data.data())

    def size(self):
        return self.m_data.size()

    def render(self, *args, **kwargs):
        return self.m_data.render(*args, **kwargs)

    def text(self, rect):
        return self.m_data.text(rect)

    def search(self, string):
        return self.m_data.search(string)

    def document(self):
        return self.m_document

    def setDocument(self, document):
        self.m_document=document

    def removeAnnotation(self, annotation):
        self.m_data.removeAnnotation(annotation)

    def annotate(self, *args, **kwargs):
        return self.m_data.annotate(*args, **kwargs)

    def annotations(self):
        return self.m_data.annotations()

    def links(self):
        return self.m_data.links()
