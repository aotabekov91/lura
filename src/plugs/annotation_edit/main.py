from PyQt6 import QtCore
from plug import Plug, tag

from .view import EditorView
from .overlay import OverlayView

class AnnotationEdit(Plug):

    default_color=(1, 0.8, 0.8)

    def setup(self):
        super().setup()
        self.setupView()

    def setupView(self):
        overlay=OverlayView(
                app=self.app,
                view=self.app.view.main,
                )
        self.view = EditorView(
            app=self.app,
            parent=overlay,
            manager=overlay,
            objectName='OverlayEdit',
            )
        self.view.m_wmap={
                'id': {'w': 'Label', 'p': '0x0x1x1'}, 
                'text' : {'w': 'TextEdit', 'p': '1x0x1x1'}}

    def mapToView(self, view, x, y):
        point=QtCore.QPoint(x, y)
        return self.mapToUI(point, view, self.app.view.main)

    def edit(self, view, annotation, x=None, y=None, w=150, h=150):
        boxes=annotation['box']
        if not x and boxes:
            box=boxes[0]
            item=annotation['item']
            bottom_right=box.bottomRight()
            bottom_right=item.mapToItem(bottom_right, unified=True)
            x=int(bottom_right.x())
            y=int(bottom_right.y())
        else:
            x=y=100
        top_left=self.mapToView(view, x, y)
        self.view.move(top_left)
        if w:
            size=QtCore.QSize(w, h)
            geometry=QtCore.QRect(top_left, size)
            self.view.setGeometry(geometry)
        self.view.setElement(annotation)
        self.view.toggle()
        self.app.stateman.toggle('input')
        # todo :current:

    @tag('<c-[>(input)')
    def test(self):
        raise

    def mapToUI(self, point, ui, match):
        parent = ui.parent()
        if not parent:
            return point
        elif ui==match:
            return point
        current = ui.mapToParent(point)
        return self.mapToUI(current, parent, match)

    @tag("<c-t>(normal)")
    def textize(self, xrange=[1]):
        view=self.app.stateman.view()
        selector=self.app.plugman.getPlug('Selection')
        if selector:
            selection=selector.selection(view=view)
            self.edit(view, selection)

        # selector=self.app.plugman.getPlug('Selection')
        # if selector:
        #     selection=selector.selection(view=view)
        #     key=xrange[0]
        #     color=self.m_colors.get(key, self.default_color)
        #     textizer=self.getAgent(view=view)
        #     selection['annotation_kind']='text'
        #     selection['annotation_color']=color
        #     selection['text']='text new'
        #     return textizer.activate(view=view, selection=selection)
