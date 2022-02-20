from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from popplerqt5 import Poppler

from .page import PdfPage
from lura.render.base import Document

class PdfDocument(Document):

    def __init__(self, filePath):
        super().__init__(filePath)
        self.m_mutex=QMutex()
        self.loadDocument()

    def numberOfPages(self):
        return self.m_data.numPages()

    def isOnline(self):
        return False

    def __eq__(self, other):
        return hash(self.m_data)==hash(other.m_data)

    def __hash__(self):
        return hash(self.m_data)

    def embeddedAuthor(self):
        return self.m_data.author()

    def embeddedTitle(self):
        return self.m_data.title()

    def setAnnotations(self):
        self.m_annotations=[]
        for i, page in enumerate(self.pages()):
            for annotation in page.annotations():
                self.m_annotations+=[annotation]

    def save(self, filePath, withChanges):

        pdfConverter=self.m_data.pdfConverter()
        pdfConverter.setOutputFileName(filePath)

        if withChanges:
            condition = pdfConverter.pdfOptions() or Poppler.PDFConverter.WithChanges
            pdfConverter.setPDFOptions(condition)

        return pdfConverter.convert()
        
    def setPages(self):
        self.m_pages= []
        for i in range(self.numberOfPages()):
            page=PdfPage(self.m_data.page(i))
            page.setPageNumber(i+1)
            page.setDocument(self)
            self.m_pages+=[page]

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
            parent.appendRow([item, pageItem])

        else:

            parent.appendRow(item)

        siblingNode=node.nextSibling()

        if not siblingNode.isNull():

            self.outline(document, siblingNode, parent)

        childNode=node.firstChild()

        if not childNode.isNull():

            self.outline(document, childNode, item)

    def data(self):
        return self.m_data

    def loadDocument(self):
        data = Poppler.Document.load(self.m_filePath)
        if data is not None:
            data.setRenderHint(Poppler.Document.Antialiasing)
            data.setRenderHint(Poppler.Document.TextAntialiasing)
            self.m_data = data
            self.setPages()
            self.setAnnotations()
            return self

    def color(self):
        if not hasattr(self, 'm_color'): return QColor('#23f2c3')
        return self.m_color

    def setColor(self, color):
        self.m_color=color
