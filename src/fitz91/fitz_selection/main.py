from PyQt6 import QtCore, QtGui

from plug import Plug

class FitzSelection(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        selection=self.app.plugman.plugs.get('Selection')
        if selection:
            selection.addAgent('FitzView', self)

    def deselect(self, model, data, view=None):
        raise

    def select(self, model, data, view=None):
        raise


    def setup(self):
        self.m_selected = []
        self.select_color = "green"
        self.select_color_alpha = 50
        super().setup()
        self.painted.connect(self.paintSelection)
        self.select_color = QtGui.QColor(self.select_color)
        self.select_color.setAlpha(self.select_color_alpha)
        self.m_select_brush = QtGui.QBrush(
            self.select_color
        )
        self.m_select_pen = QtGui.QPen(self.select_color)

    def selection(self):
        return self.m_selected

    def select(self, s=[], append=False):
        if type(s) != list:
            s = [s]
        if append:
            self.m_selected += s
        else:
            self.m_selected = s
        self.refresh()

    def paintSelection(self, painter, ops, widget, item):
        if self.m_selected:
            painter.save()
            for item in self.m_selected:
                boxes = item.get("box", [])
                rects = []
                if type(boxes)!=list:
                    boxes=[boxes]
                for box in boxes:
                    rects += [
                        self.mapToItem(box, unified=True)
                    ]
                painter.setBrush(self.m_select_brush)
                painter.drawRects(rects)
                painter.setPen(self.m_select_pen)
                painter.drawRects(rects)
            painter.restore()
            self.selectionPainted.emit(painter, ops, widget, item)
