from PyQt6 import QtCore


class SinglePage:
    def __init__(
        self,
        config={},
        pageSpacing=0,
        viewportPadding=0,
        **kwargs,
    ):
        self.m_config = config
        self.pageSpacing = pageSpacing
        self.viewportPadding = viewportPadding
        self.setSettings()

    def setSettings(self):
        c = self.m_config
        for k, v in c.items():
            setattr(self, k, v)

    def left(self, idx, count=None):
        return idx

    def right(self, idx, count=None):
        return idx

    def up(self, idx, count=None):
        return idx

    def down(self, idx, count=None):
        return idx

    def next(self, idx, count=None):
        return min(idx + 1, count)

    def prev(self, idx, count=None):
        return max(idx - 1, 1)

    def current(self, idx, count=None):
        return idx

    def width(self, width):
        ps = self.pageSpacing
        return width - self.viewportPadding - 2.0 * ps

    def height(self, height):
        return height - 2.0 * self.pageSpacing

    def itemsAt(
        self,
        rect,
        items,
    ):
        for i in items.values():
            if i.m_rect.intersects(rect):
                yield i

    def load(
        self,
        items,
        x,
        right,
        height,
        *args,
        **kwargs,
    ):
        ph = 0.0
        ps = self.pageSpacing
        for i in items.values():
            br = i.boundingRect()
            x = -br.left() - 0.5 * br.width()
            y = height - br.top()
            w, h = br.width(), br.height()
            i.setPos(x, y)
            if hasattr(i, "m_rect"):
                i.m_rect.setX(x)
                i.m_rect.setY(y)
                i.m_rect.setWidth(w)
                i.m_rect.setHeight(h)
            ph = br.height()
            x = min(x, -0.5 * br.width())
            right = max(right, 0.5 * br.width())
            height += ps + ph
        return x, right, height
