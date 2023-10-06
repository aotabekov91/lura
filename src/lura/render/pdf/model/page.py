from PyQt5 import QtCore, QtGui

from popplerqt5 import Poppler
from .annotation import Annotation

class Page(QtCore.QObject):

    annotationAdded=QtCore.pyqtSignal(object)
    annotationRemoved=QtCore.pyqtSignal(object)

    def __init__(self, popplerPage, pageNumber, document):

        super(Page, self).__init__()

        self.m_annotations=[]
        self.m_document=document
        self.m_data = popplerPage
        self.m_pageNumber=pageNumber

        self.m_normalizedTransform=QtGui.QTransform()
        self.m_normalizedTransform.reset()
        self.m_normalizedTransform.scale(
                self.size().width(), 
                self.size().height())

        self.m_native_annotations=self.getNativeAnnotations()

    def document(self): return self.m_document

    def pageNumber(self): return self.m_pageNumber

    def pageItem(self): return self.m_pageItem

    def setPageItem(self, pageItem): self.m_pageItem=pageItem

    def size(self): return self.m_data.pageSizeF()

    def render(self, hResol=72, vResol=72, rotate=0, boundingRect=None):

        x, y, w, h = (-1,)*4

        if boundingRect is not None:
            x = int(boundingRect.x())
            y = int(boundingRect.y())
            w = int(boundingRect.width())
            h = int(boundingRect.height())

        return self.m_data.renderToImage(hResol, vResol, x, y, w, h, rotate)

    def find(self, rect, unified=False): 

        if unified: rect=self.m_normalizedTransform.mapRect(rect)
        return self.m_data.text(rect)

    def search(self, string): 

        return self.m_data.search(string, Poppler.Page.CaseInsensitive)

    def annotate(self, aData, kind, **kwargs):

        color=aData['color']
        boundary=aData['boundaries']

        if kind=='highlightAnnotation':
            annotation=self.addHighlightAnnotation(boundary, color)
        elif kind=='textAnnotation':
            annotation=self.addTextAnnotation(boundary, color)

        aData['pAnn']=annotation
        self.m_annotations+=[aData]

        return aData

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
        bound=QtCore.QRectF()
        for b in boundary: 
            bound=bound.united(b)
        annotation=Poppler.HighlightAnnotation()
        annotation.setHighlightQuads(quads)
        annotation.setStyle(style)
        annotation.setBoundary(bound)
        self.m_data.addAnnotation(annotation)
        ann=Annotation(annotation)
        ann.setPage(self)
        return ann

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
        ann=Annotation(annotation)
        ann.setPage(self)
        return ann

    def removeAnnotation(self, aData):

        aid=aData.get('id')

        if aid:

            for data in self.m_annotations:
                if data['id']==aid:
                    self.m_annotations.pop(self.m_annotations.index(data))
                    self.m_data.removeAnnotation(data['pAnn'].data())
                    self.annotationRemoved.emit(self)

    def nativeAnnotations(self): return self.m_native_annotations

    def getNativeAnnotations(self):

        annotations=[]

        for data in self.m_data.annotations():
            kind = data.subType()
            cond = kind in [
                Poppler.Annotation.AText,
                Poppler.Annotation.AHighlight,
                Poppler.Annotation.AFileAttachment]
            if cond:
                data.setContents(self.find(data.boundary(), unified=True))
                annotation=Annotation(data)
                annotation.setPage(self)
                annotations+=[annotation]

        return annotations

    def annotations(self): return self.m_annotations

    def links(self):

        links = []
        for link in self.m_data.links():
            boundary = link.linkArea().normalized()
            data={}
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
                    data={'boundary': boundary, 'file': linkGoto.fileName(), 'page': page}
                else:
                    data={'boundary': boundary, 'page': page, 'left': left, 'top': top}


            elif link.linkType() == Poppler.Link.Browse:
                linkBrowse = link
                url = linkBrowse.url()
                data={'boundary': boundary, 'url': url}
            elif link.linkType() == Poppler.Link.Execute:
                url = link.fileName()
                data={'boundary': boundary, 'path': url}

            if data:

                data['sourcePage'] = self.pageNumber()
                links.append(data)

        return links

    def data(self): return self.m_data

    def getRows(self, start, end):

        if start.y()==end.y():
            rect=QtCore.QRectF()
            if start.x()<end.x():
                rect.setTopLeft(start.topLeft())
                rect.setBottomRight(end.bottomRight())
            elif start.x()>=end.x():
                rect.setTopLeft(end.topLeft())
                rect.setBottomRight(start.bottomRight())
            area=[rect]

        else:

            if start.y()<end.y():
                up, down=start, end
            else:
                up, down=end, start

            rects={}
            for b in self.data().textList():
                box=b.boundingBox()
                if box.y()>=up.y() and box.y()<=down.y():
                    if box.y()==up.y():
                        if box.x()<up.x(): continue
                    if box.y()==down.y():
                        if box.x()+box.width()>down.x()+down.width(): continue

                    if not box.y() in rects: rects[box.y()]=box

                    r=rects[box.y()]

                    if box.x()<r.x(): 
                        r.setTopLeft(box.topLeft())

                    if box.x()+box.width()>r.x()+r.width():
                        r.setBottomRight(box.bottomRight())

            area=list(rects.values())

        text=[]

        for a in area: text+=[self.find(a)]

        data=[]
        for t in self.data().textList():
            for a in area: 
                if a.contains(t.boundingBox()): data+=[t]

        return {'box':area, 'text': ' '.join(text), 'data':data}

    def getRow(self, point):

        for tData in self.data().textList():
            if tData.boundingBox().contains(point):
                return {'data': [tData], 'box':[tData.boundingBox()], 'text':tData.text()}

    def textList(self): return self.data().textList()
