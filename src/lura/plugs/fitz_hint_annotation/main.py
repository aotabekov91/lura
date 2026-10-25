from PyQt6 import QtCore, QtGui

from plug import Plug, deleg

class FitzAnnotationHint(Plug):

    def setup(self):
        super().setup()
        self.m_hint=''
        self.m_hints={}
        self.m_element_hints={}

    @deleg('activate@(hint[annotation])[FitzView]')
    def activate(self, view=None, **kwargs):
        if view:
            super().activate()
            self.app.stateman.setFunctor(functor=self.functor)
            view.itemPainted.connect(self.paint)
            self.assignHints(view)
            view.redraw()

    @deleg('octivate@(hint[annotation])[FitzView]')
    def octivate(self, view=None, **kwargs):
        if view:
            super().octivate()
            self.m_hint=''
            self.m_element_hints={}
            self.app.stateman.setFunctor()
            view.itemPainted.disconnect(
                    self.paint)
            view.redraw()

    def assignHints(self, view=None, kind='letters'):
        annotations=[]
        if view:
            model=view.model()
            amodel=self.app.delegman.delegate(
                    mode='annotate', 
                    action='getModel',
                    data={'model': model})
            if amodel:
                items=view.visibleItems()
                for item in items: 
                    element=item.element()
                    idx=element.index()
                    item_annotations=amodel.get(
                            idx, by='page', only_one=False)
                    annotations+=item_annotations
                moder=self.app.stateman.moder()
                _, hints=moder.generateHints(annotations, kind)
                if hints:
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
                    return annotations
            self.app.delegman.delegate(
                    mode='hint', action='normal', data={'view': view})
        return annotations

    def paint(self, painter, ops, widget, item):
        painter.save()
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.red, 0.0)
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
        return self.m_hint==hint[:len(self.m_hint)]

    def functor(self, key, earman):
        self.m_hint=key
        view=self.app.stateman.view()
        if key in self.m_hints:
            annotation=self.m_hints.get(key)
            self.select(view, annotation)
            # self.edit(annotation, view)
            view.redraw()
            return True
        for hint in self.m_hints:
            if self.checkHint(hint):
                view.redraw()
                return True
        self.m_hint=''
        view.redraw()
        return False

    # todo: move it to edit[annotation]
    # def edit(self, annotation, view, **kwargs):
    #     agent=self.app.plugman.getPlug('AnnotationHint')
    #     agent.octivate()
    #     agent=self.app.plugman.getPlug('AnnotationEdit')
    #     if agent:
    #         agent.activate(view=view, annotation=annotation, **kwargs)

    def select(self, view, annotation):
        data=annotation.data()
        element = data["element"]
        idx=element.index()
        data['item']=view.item(idx)
        self.app.delegman.delegate(
                action='setSelection', 
                data={'view': view, 'selection': annotation})
        self.app.delegman.delegate(
                mode='hint', action='normal', data={'view': view})
