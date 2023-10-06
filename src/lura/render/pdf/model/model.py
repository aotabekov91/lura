from popplerqt5 import Poppler
from PyQt5 import QtCore, QtGui

from .page import Page

class Model(QtCore.QObject):

    def __init__(self, filePath):

        super().__init__()
        self.m_data=None
        self.m_hash=None
        self.m_mutex=QtCore.QMutex()
        self.m_filePath=filePath
        self.readFilepath(filePath)

    def readFilepath(self, filePath):

        (d, p) =self.loadDocument(filePath)
        self.m_data, self.m_pages= (d, p)

    def loadDocument(self, filePath):

        m_data = Poppler.Document.load(filePath)
        if m_data:
            m_data.setRenderHint(Poppler.Document.Antialiasing)
            m_data.setRenderHint(Poppler.Document.TextAntialiasing)
            m_pages=self.setPages(m_data)
            return m_data, m_pages
        else:
            return None, {}

    def nativeAnnotations(self):

        annotations=[]
        for pageNumber, page in self.m_pages.items():
            annotations+=page.nativeAnnotations()
        return annotations

    def annotations(self):

        annotations=[]
        for pageNumber, page in self.m_pages.items():
            annotations+=page.annotations()
        return annotations

    def save(self, filePath, withChanges):

        pdfConverter=self.m_data.pdfConverter()
        pdfConverter.setOutputFileName(filePath)

        if withChanges:
            condition = pdfConverter.pdfOptions() or Poppler.PDFConverter.WithChanges
            pdfConverter.setPDFOptions(condition)

        return pdfConverter.convert()


    def setPages(self, m_data):

        m_pages={}
        for i in range(m_data.numPages()):
            page=Page(m_data.page(i), pageNumber=i+1, document=self)
            m_pages[i+1] = page
        return m_pages

    def search(self, text):

        found={}
        for i, page in enumerate(self.pages()):
            match=page.search(text)
            if len(match)>0:
                found[i]=match
        return found

    def loadOutline(self):

        toc=self.m_data.toc()
        outlineModel=QtGui.QStandardItemModel()
        if toc!=0:
            try:
                self.outline(
                        self.m_data,
                        toc.firstChild(),
                        outlineModel.invisibleRootItem()
                        )
            except:
                pass
        return outlineModel

    def outline(self, document, node, parent):

        element=node.toElement()
        item=QtGui.QStandardItem(element.tagName())
        item.setFlags(QtCore.Qt.ItemIsEnabled or QtCore.Qt.ItemIsSelectable)

        linkDestination=0

        if element.hasAttribute('Destination'):
            linkDestination=Poppler.LinkDestination(
                    element.attribute('Destination'))
        elif element.hasAttribute('DestinationName'):
            linkDestination=self.m_data.linkDestination(
                    element.attribute('DestinationName'))

        if linkDestination!=0:

            page=linkDestination.pageNumber()
            left=0.
            top=0.

            if page<1: page=1

            if page>document.numPages(): page=document.numPages()

            if linkDestination.isChangeLeft():

                left=linkDestination.left()

                if left<0.: left=0.
                if left>1.: left=1.

            if linkDestination.isChangeTop():

                top=linkDestination.top()

                if top<0.: top=0.
                if top>1.: top=1.

            del linkDestination

            item.setData(page, QtCore.Qt.UserRole+1)
            item.setData(left, QtCore.Qt.UserRole+2)
            item.setData(top, QtCore.Qt.UserRole+3)
            item.setData(element.tagName(), QtCore.Qt.UserRole+5)

            pageItem=item.clone()
            pageItem.setText(str(page))
            pageItem.setTextAlignment(QtCore.Qt.AlignRight)

            # if allow also pages the look of outline becomes ugly
            # parent.appendRow([item, pageItem])
            parent.appendRow(item)

        siblingNode=node.nextSibling()

        if not siblingNode.isNull():
            self.outline(document, siblingNode, parent)

        childNode=node.firstChild()

        if not childNode.isNull():
            self.outline(document, childNode, item)

    def __eq__(self, other): return self.m_data==other.m_data

    def __hash__(self): return hash(self.m_data)

    def id(self): return self.m_id

    def setId(self, m_id): self.m_id=m_id

    def filePath(self): return self.m_filePath

    def readSuccess(self): return self.m_data is not None

    def numberOfPages(self): return self.m_data.numPages()

    def setHash(self, dhash): self.m_hash=dhash

    def hash(self): return self.m_hash

    def author(self): return self.m_data.author()

    def title(self): return self.m_data.title()

    def page(self, pageNumber): return self.m_pages.get(pageNumber, None)

    def pages(self): return self.m_pages
