from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from popplerqt5 import Poppler

class PdfAnnotation(QObject):

    def __init__(self, annotationData):
        super().__init__()
        self.m_data = annotationData

    def id(self):
        return self.m_id

    def setId(self, m_id):
        self.m_id=m_id

    def color(self):
        return self.m_data.style().color()

    def type(self):
        return self.m_data.subType()

    def data(self):
        return self.m_data

    def setData(self, data):
        self.m_data=data

    def boundary(self):
        return self.m_data.boundary().normalized()

    def position(self):
        return '{}:{}:{}:{}'.format(
            round(self.boundary().x(), 8),
            round(self.boundary().y(), 8),
            round(self.boundary().width(), 8),
            round(self.boundary().height(), 8))

    def content(self):
        return self.m_data.contents()

    def setColor(self, color):
        style.setColor(color)
        self.m_data.setStyle(style)

    def setContent(self, text):
        self.m_data.setContents(text)

class PdfDocument:

    def __init__(self, popplerDocument):
        self.m_data = popplerDocument
        self.setPages()
        self.m_mutex=QMutex()

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
        pAnnotations=page.annotations()
        for annotation in pAnnotations:
            annotations+=[PdfAnnotation(annotation)]
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
            self.m_pages += [PdfPage(self.m_data.page(i))]

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

    def __eq__(self, other):
        return self.m_data==other.m_data

    def __hash__(self):
        return hash(self.m_data)

    def id(self):
        return self.m_id

    def setId(self, m_id):
        self.m_id=m_id

class PdfPage:

    def __init__(self, popplerPage):
        self.m_data = popplerPage

    def size(self):
        return self.m_data.pageSizeF()

    def render(self, hResol=72, vResol=72, rotate=0, boundingRect=None):
        x, y, w, h = (-1,)*4

        if boundingRect is not None:
            x = boundingRect.x()
            y = boundingRect.y()
            w = boundingRect.width()
            h = boundingRect.height()

        return self.m_data.renderToImage(hResol, vResol, x, y, w, h, rotate)

    def text(self, rect):
        return self.m_data.text(rect)

    def search(self, string):
        return self.m_data.search(string)

    def annotate(self, boundary, color, kind, *args, **kwargs):
        if kind=='highlightAnnotation':
            return self.addHighlightAnnotation(boundary, color)
        elif kind=='textAnnotation':
            return self.addTextAnnotation(boundary, color)

    def addHighlightAnnotation(self, boundary, color):

        style=Poppler.Annotation.Style()
        style.setColor(color)
        popup=Poppler.Annotation.Popup()
        popup.setFlags(Poppler.Annotation.Hidden or
                Poppler.Annotation.ToggleHidingOnMouse)

        if not type(boundary)==list:
            boundary=[boundary]

        quads=[]

        for bound in boundary:
            quad = Poppler.HighlightAnnotation.Quad()
            quad.points = [bound.topLeft(),
                           bound.topRight(),
                           bound.bottomRight(),
                           bound.bottomLeft()]
            quads+=[quad]

        bound=QRectF()
        for b in boundary:
            bound=bound.united(b)

        annotation=Poppler.HighlightAnnotation()
        annotation.setHighlightQuads(quads)
        annotation.setStyle(style)
        annotation.setBoundary(bound)
        self.m_data.addAnnotation(annotation)
        return PdfAnnotation(annotation)

    def addTextAnnotation(self, boundary, color):

        style=Poppler.Annotation.Style()
        style.setColor(color)
        popup=Poppler.Annotation.Popup()
        popup.setFlags(Poppler.Annotation.Hidden or
                Poppler.Annotation.ToggleHidingOnMouse)

        annotation=Poppler.TextAnnotation(Poppler.TextAnnotation.Linked)

        annotation.setBoundary(boundary)
        annotation.setStyle(style)
        annotation.setPopup(popup)

        self.m_data.addAnnotation(annotation)
        return PdfAnnotation(annotation)

    def removeAnnotation(self, annotation):
        for rAnnotation in self.annotations():
            if rAnnotation.boundary()!=annotation.boundary(): continue
            self.m_data.removeAnnotation(rAnnotation.data())

    def annotations(self):

        annotations = []

        for annotation in self.m_data.annotations():
            kind = annotation.subType()
            cond = kind in [
                Poppler.Annotation.AText,
                Poppler.Annotation.AHighlight,
                Poppler.Annotation.AFileAttachment]
            if cond:
                annotations.append(PdfAnnotation(annotation))
        return annotations


    def links(self):
        links = []
        for link in self.m_data.links():
            boundary = link.linkArea().normalized()
            if link.linkType() == Poppler.Link.Goto:
                linkGoto = link
                page = linkGoto.destination().pageNumber()

                left = 0.
                if linkGoto.destination().isChangeLeft():
                    left = linkGoto.destination().left()
                top = 0.
                if linkGoto.destination().isChangeTop():
                    top = linkGoto.destination().top()
                if not 0 <= left <= 1:
                    left = (left > 1.)*1.+(left < 0.)*0.
                if not 0 <= top <= 1:
                    top = (top > 1.)*1.+(top < 0.)*0.

                if linkGoto.isExternal():
                    links.append({'boundary': boundary,
                                  'file': linkGoto.fileName(),
                                  'page': page})
                else:
                    links.append({'boundary': boundary,
                                  'page': page,
                                  'left': left,
                                  'top': top})
            elif link.linkType() == Poppler.Link.Browse:
                linkBrowse = link
                url = linkBrowse.url()
                links.append({'boundary': boundary,
                              'url': url})
            elif link.linkType() == Poppler.Link.Execute:
                url = link.fileName()
                lins.append({'boundary': boundary,
                             'url': url})
        return links

    def data(self):
        return self.m_data


class PdfPlugin:

    def loadDocument(filePath):
        data = Poppler.Document.load(filePath)
        if data is not None:
            data.setRenderHint(Poppler.Document.Antialiasing)
            data.setRenderHint(Poppler.Document.TextAntialiasing)
            document = PdfDocument(data)
            return document
