from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from popplerqt5 import Poppler

from .page import PdfPage
from .annotation import PdfAnnotation

class PdfDocument(QObject):

    def __init__(self, filePath):
        super().__init__()
        self.m_filePath=filePath
        self.loadDocument()
        self.m_mutex=QMutex()

    def loadDocument(self):
        self.m_data = Poppler.Document.load(self.m_filePath)
        if self.m_data is not None:
            self.m_data.setRenderHint(Poppler.Document.Antialiasing)
            self.m_data.setRenderHint(Poppler.Document.TextAntialiasing)
            self.setPages()
        else:
            self.m_data=None

    def filePath(self):
        return self.m_filePath

    def readSuccess(self):
        return self.m_data is not None

    def numberOfPages(self):
        return self.m_data.numPages()

    def author(self):
        return self.m_data.author()

    def title(self):
        return self.m_data.title()

    def page(self, index):
        page = self.m_data.page(index)
        if page is not None:
            return PdfPage(page)

    def annotations(self):
        annotations=[]
        for page in self.m_pages:
            annotations+=page.annotations()
        return annotations

    def save(self, filePath, withChanges):

        pdfConverter=self.m_data.pdfConverter()
        pdfConverter.setOutputFileName(filePath)

        if withChanges:
            condition = pdfConverter.pdfOptions() or Poppler.PDFConverter.WithChanges
            pdfConverter.setPDFOptions(condition)

        return pdfConverter.convert()

    def pages(self):
        return self.m_pages

    def setPages(self):
        self.m_pages= []
        for i in range(self.numberOfPages()):
            page=PdfPage(self.m_data.page(i))
            page.setDocument(self)
            page.setPageNumber(i+1)
            self.m_pages += [page]

    def search(self, text):
        found={}
        for i, page in enumerate(self.pages()):
            match=page.search(text)
            if len(match)>0:
                found[i]=match
        return found

    def loadOutline(self):
        outlineModel=QStandardItemModel()
        toc=self.m_data.toc()
        if toc!=0:
            try:
                self.outline(self.m_data, toc.firstChild(), outlineModel.invisibleRootItem())
            except:
                pass
        return outlineModel

    def outline(self, document, node, parent):

        element=node.toElement()

        item=QStandardItem(element.tagName())
        item.setFlags(Qt.ItemIsEnabled or Qt.ItemIsSelectable)

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

            item.setData(page, Qt.UserRole+1)
            item.setData(left, Qt.UserRole+2)
            item.setData(top, Qt.UserRole+3)
            item.setData(element.tagName(), Qt.UserRole+5)

            pageItem=item.clone()
            pageItem.setText(str(page))
            pageItem.setTextAlignment(Qt.AlignRight)


            # if allow also pages the look of outline becomes ugly
            # parent.appendRow([item, pageItem])
            parent.appendRow(item)

        siblingNode=node.nextSibling()

        if not siblingNode.isNull():

            self.outline(document, siblingNode, parent)

        childNode=node.firstChild()

        if not childNode.isNull():

            self.outline(document, childNode, item)

    def __eq__(self, other):
        return self.m_data==other.m_data

    def __hash__(self):
        return hash(self.m_data)

    def id(self):
        return self.m_id

    def setId(self, m_id):
        self.m_id=m_id
