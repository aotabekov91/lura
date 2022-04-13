from PyQt5.QtCore import *
from popplerqt5 import Poppler

from lura.render.base import Page
from .annotation import PdfAnnotation

class PdfPage(Page):

    def document(self):
        return self.m_document

    def setDocument(self, document):
        self.m_document=document

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
            data= self.addHighlightAnnotation(boundary, color)
        elif kind=='textAnnotation':
            data= self.addTextAnnotation(boundary, color)
        print(data.contents())
        annotation=PdfAnnotation()
        annotation.setAnnotationData(data)
        annotation.setPage(self)
        return annotation

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
        return annotation

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
        return annotation

    def removeAnnotation(self, annotation):
        for rAnnotation in self.m_data.annotations():
            if rAnnotation.boundary()!=annotation.boundary(): continue
            self.m_data.removeAnnotation(rAnnotation)

    def annotations(self):

        annotations = []

        for data in self.m_data.annotations():
            kind = data.subType()
            cond = kind in [
                Poppler.Annotation.AText,
                Poppler.Annotation.AHighlight,
                Poppler.Annotation.AFileAttachment]
            if cond: 
                annotation=PdfAnnotation()
                annotation.setAnnotationData(data)
                annotation.setPage(self)
                annotations+=[annotation]
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
