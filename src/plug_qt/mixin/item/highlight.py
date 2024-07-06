from PyQt6 import QtGui


class Highlight:
    canHighlight = True

    def setup(self):
        self.color_alpha = 90
        self.m_highlighted = None
        self.highlight_color = "green"
        super().setup()
        self.highlight_color = QtGui.QColor(
            self.highlight_color
        )
        self.highlight_color.setAlpha(self.color_alpha)
        self.m_brush = QtGui.QBrush(self.highlight_color)
        self.painted.connect(self.paintHighlight)

    def highlighted(self):
        return self.m_highlighted

    def highlight(self, h=None):
        self.m_highlighted = h
        self.update()

    def paintHighlight(self, p, o, w, i):
        if self.m_highlighted:
            p.save()
            box = self.m_highlighted.get("box", [])
            for s in box:
                p.setBrush(self.m_brush)
                si = self.mapToItem(s, unified=True)
                p.drawRects(si)
            p.restore()
