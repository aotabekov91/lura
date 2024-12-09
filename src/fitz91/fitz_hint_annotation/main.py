from PyQt6 import QtCore, QtGui

from plug import Plug

class FitzAnnotationHint(Plug):

    def setup(self):
        super().setup()
        self.m_hint=''
        self.m_hints={}
        self.m_element_hints={}
        if self.app.running:
            self.addHinter()
        else:
            self.app.appSoonStarts.connect(
                    self.addHinter)

    def addHinter(self):
        annotator=self.app.plugman.getPlug('Annotate')
        hinter=self.app.plugman.getPlug('AnnotationHint')
        if hinter and annotator:
            hinter.addAgent('FitzView', self)

    def assignHints(self, view):
        annotations=[]
        model=view.model()
        items=view.visibleItems()
        hinter=self.app.plugman.getPlug('Hint')
        annotator=self.app.plugman.getPlug('Annotate')
        annotation_model=annotator.getModel(model)
        for item in items: 
            element=item.element()
            idx=element.index()
            item_annotations=annotation_model.getAnnotate(
                    idx, by='page', only_one=False)
            annotations+=item_annotations
        _, hints=hinter.generateHints(annotations)
        self.m_hints=hints
        self.m_element_hints={}
        for hint, annotation in hints.items():
            data=annotation.data()
            data['hint']=hint
            element=data['element']
            idx=element.index()
            if not idx in self.m_element_hints:
                self.m_element_hints[idx]=[]
            self.m_element_hints[idx]+=[data]

    def activate(self, view=None, **kwargs):
        if view:
            self.assignHints(view)
            self.app.stateman.setFunctor(functor=self.functor)
            view.itemPainted.connect(self.paint)
            view.redraw()

    def octivate(self, view=None, **kwargs):
        if view:
            self.m_hint=''
            self.m_element_hints={}
            self.app.stateman.setFunctor()
            view.itemPainted.disconnect(
                    self.paint)
            view.redraw()

    def paint(self, painter, ops, widget, item):
        painter.save()
        pen = QtGui.QPen(
                QtCore.Qt.GlobalColor.red, 0.0)
        painter.setPen(pen)
        element=item.element()
        idx=element.index()
        annotations=self.m_element_hints.get(idx, [])
        for data in annotations:
            hint=data.get("hint")
            box = data.get("box")[0]
            if not self.checkHint(hint):
                continue
            rect =item.mapToItem(box, unified=True)
            painter.drawText(rect.topLeft(), hint)
        painter.restore()

    def checkHint(self, hint):
        partial=hint[:len(self.m_hint)]
        return self.m_hint==partial

    def functor(self, key, earman):
        self.m_hint=key
        view=self.app.stateman.view()
        if key in self.m_hints:
            annotation=self.m_hints.get(key)
            self.select(annotation, view)
            self.edit(annotation, view)
            view.redraw()
            return True
        for hint in self.m_hints:
            if self.checkHint(hint):
                view.redraw()
                return True
        self.m_hint=''
        view.redraw()
        return False

    def edit(self, annotation, view, **kwargs):
        agent=self.app.plugman.getPlug('AnnotationHint')
        agent.octivate()
        agent=self.app.plugman.getPlug('AnnotationEdit')
        if agent:
            agent.activate(view=view, annotation=annotation, **kwargs)

    def select(self, annotation, view):
        data=annotation.data()
        element = data["element"]
        idx=element.index()
        data['item']=view.item(idx)
        selector=self.app.plugman.getPlug('Selection')
        if selector:
            selector.select(view, selection=annotation)
