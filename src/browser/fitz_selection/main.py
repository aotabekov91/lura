from PyQt6 import QtGui

from plug import Plug

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
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        selector=self.app.plugman.getPlug('Selection')
        if selector:
            selector.addAgent('FitzView', self)

    def wire(self, view, kind='connect'):
        item, _ =self.m_views.get(view, (None, None))
        if item and kind=='connect':
            item.painted.connect(self.paint)
        elif item and kind=='disconnect':
            item.painted.disconnect(self.paint)

    def select(self, view, selection):
        item=selection['item']
        current_item, current_selection=self.m_views.get(view, (None, None))
        cond1=item and current_item!=item
        cond2=item and current_selection!=selection
        if cond1 or cond2:
            self.wire(view, 'disconnect')
            self.m_views[view]=(item, selection)
            self.wire(view, 'connect')
        elif not item and current_item:
            self.wire(view, 'disconnect')
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
