from PyQt6 import QtGui

from plug import Plug, deleg

class FitzSelection(Plug):

    select_color = "green"
    select_color_alpha = 50

    def setup(self):
        super().setup()
        self.m_views={}
        self.select_color = QtGui.QColor(self.select_color)
        self.select_color.setAlpha(self.select_color_alpha)
        self.m_select_brush = QtGui.QBrush(self.select_color)
        self.m_select_pen = QtGui.QPen(self.select_color)

    def connect(self, view, kind='connect'):
        item, _ =self.m_views.get(view, (None, None))
        if item and kind=='connect':
            item.painted.connect(self.paint)
        elif item and kind=='disconnect':
            item.painted.disconnect(self.paint)

    @deleg('select@(any)[FitzView]')
    def select(self, view=None, selection=None, **kwargs):
        if view and selection:
            item=selection['item']
            current_item, current_selection=self.m_views.get(view, (None, None))
            cond1=item and current_item!=item
            cond2=item and current_selection!=selection
            if cond1 or cond2:
                self.connect(view, 'disconnect')
                self.m_views[view]=(item, selection)
                self.connect(view, 'connect')
            elif not item and current_item:
                self.connect(view, 'disconnect')
                self.m_views.pop(view, None)
            view.redraw()

    def paint(self, painter, ops, widget, item):
        view=item.view()
        current_item, selection=self.m_views.get(view, (None, None))
        if selection and item==current_item:
            painter.save()
            rects = []
            boxes = selection["box"] or []
            if type(boxes)!=list:
                boxes=[boxes]
            for box in boxes:
                rects += [item.mapToItem(box, unified=True)]
            painter.setBrush(self.m_select_brush)
            painter.drawRects(rects)
            painter.setPen(self.m_select_pen)
            painter.drawRects(rects)
            painter.restore()
