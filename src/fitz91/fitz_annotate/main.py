import fitz
from PyQt6 import QtCore

from plug import Plug

class FitzAnnotate(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addToAnnotate()
        else:
            self.app.appSoonStarts.connect(
                    self.addToAnnotate)

    def addToAnnotate(self):
        annotate=self.app.plugman.plugs.get('Annotate')
        if annotate:
            annotate.addAgent('FitzModel', self)

    def open(self, view, data={}, center=True):
        boxes = data.get("box", None)
        page = data.get("page", None)
        if all([view, page, boxes]):
            item = view.item(page)
            top_left = boxes[0].topLeft()
            view.goTo(page, top_left.x(), top_left.y(), center=center)
            view.select(item, data)

    def deannotate(self, view, data):
        box = data["box"][0]
        box = self.m_norm.mapRect(box)
        for annotation in self.m_data.annots():
            rect=annotation.rect
            p1 = QtCore.QPointF(rect.x0, rect.y0)
            p2 = QtCore.QPointF(rect.x1, rect.y1)
            r = QtCore.QRectF(p1, p2)
            if r.intersects(box):
                self.m_data.delete_annot(annotation)
                self.m_model.clearPixmapCache(idx=self.index())
                return annotation

    def setPage(self, model, data):
        page = data.get("page", None)
        item = data.get("item", None)
        element = data.get("element", None)
        if element:
            page=element.index()
            data["page"] = page
        elif item:
            element = item.element()
            page=element.index()
            data["page"] = page
            data["element"] = model.element(page)
        elif page:
            data["element"] = model.element(page)

    def annotate(self, model, data, view=None):
        annotation = None
        boxes=data.get("box")
        kind=data.get("annotation_kind")
        color=data.get("annotation_color", None)
        self.setPage(model, data)
        data=model.getLocator(data=data, kind='uniq')
        element=data.get('element')
        if element:
            element_data = element.data()
            quads = self.getQuads(data)
            if kind == "highlight":
                annotation = element_data.add_highlight_annot(quads)
            elif kind == "underline":
                annotation = element_data.add_underline_annot(quads)
            elif kind == "strike-out":
                annotation = element_data.add_strikeout_annot(quads)
            elif kind == "caret" and boxes:
                quad = quads[0]
                annotation = element_data.add_caret_annot(quad.ul)
            elif kind == "text" and boxes:
                quad = quads[0]
                text=data.get("text", "")
                annotation = element_data.add_text_annot(quad.ul, text)
            if annotation:
                if color:
                    annotation.set_colors(stroke=color)
                annotation.update()
                model.clearPixmapCache(idx=element.index())
                # element.dataChanged.emit()
            if view:
                view.cleanUpSelection()
                view.redraw()
            return data

    def getQuads(self, data):
        quads = []
        boxes = data.get("box")
        element=data.get("element", None)
        for box in boxes:
            box=element.unity(box)
            x, y = box.x(), box.y()
            w, h = box.width(), box.height()
            ul, ur = (x, y), (x + w, y)
            ll, lr = (x, y + h), (x + w, y + h)
            quads += [fitz.Quad(ul, ur, ll, lr)]
        return quads
