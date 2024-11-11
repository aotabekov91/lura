from PyQt6 import QtGui

from plug import Plug

class FitzSelection(Plug):

    select_color = "green"
    select_color_alpha = 50

    def setup(self):
        super().setup()
        self.m_views={}
        self.m_items={}
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
        selector=self.app.plugman.plugs.get('Selection')
        if selector:
            selector.addAgent('FitzView', self)

    def wire(self, view, kind='connect'):
        item=self.m_views.get(view, None)
        if item and kind=='connect':
            item.painted.connect(self.paint)
        elif item and kind=='disconnect':
            item.painted.disconnect(self.paint)

    def select(self, view, data):
        self.wire(view, 'disconnect')
        item=data['item']
        self.m_views[view]=item
        self.m_items[item]=data
        self.wire(view, 'connect')

    def deselect(self, view):
        self.wire(view, 'disconnect')
        view.redraw()

    def paint(self, painter, ops, widget, item):
        data=self.m_items.get(item, None)
        if data:
            painter.save()
            boxes = data.get("box", [])
            rects = []
            if type(boxes)!=list:
                boxes=[boxes]
            for box in boxes:
                rects += [item.mapToItem(box, unified=True)]
            painter.setBrush(self.m_select_brush)
            painter.drawRects(rects)
            painter.setPen(self.m_select_pen)
            painter.drawRects(rects)
            painter.restore()
