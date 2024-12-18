import fitz

from plug import Plug

class FitzAnnotate(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        annotate=self.app.plugman.getPlug('Annotate')
        if annotate:
            annotate.addAgent('FitzModel', self)

    def goTo(self, view, data, center=True):
        boxes = data.get("box", None)
        page = data.get("page", None)
        if all([view, page, boxes]):
            top_left = boxes[0].topLeft()
            selector=self.app.plugman.getPlug('Selection')
            view.goTo(page, top_left.x(), top_left.y(), center=center)
            if selector:
                selector.select(view, **data)

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

    def deannotate(self, model, data):
        element=data.get('element')
        annotation=data.get('annotation_object')
        if element and annotation:
            page_data=element.data()
            page_data.delete_annot(annotation)
            model.clearPixmapCache(idx=element.index())
            return annotation

    def annotate(self, model, data):
        annotation = None
        boxes=data.get("box")
        kind=data.get("annotation_kind")
        color=data.get("annotation_color", None)
        self.setPage(model, data)
        element=data.get('element')
        if element:
            element_data = element.data()
            quads = self.getQuads(data)
            if kind == "highlight":
                annotation = element_data.add_highlight_annot(quads)
            elif kind == "underline":
                annotation = element_data.add_underline_annot(quads)
            elif kind == "strikeout":
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
                data['annotation_object']=annotation
                annotation.update()
                model.clearPixmapCache(idx=element.index())
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
