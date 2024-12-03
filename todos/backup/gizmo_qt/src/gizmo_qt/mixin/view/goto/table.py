from .base import Go


class TableWidgetGo(Go):
    def goTo(self, xrange=None, **kwargs):
        if xrange is None:
            self.goToLast()
        else:
            super().goTo(xrange=xrange, **kwargs)

    def goToUp(self, xrange=[1], **kwargs):
        if not self.m_curr:
            r, c = self.m_layout.rowCount(), 0
        else:
            r, c = self.m_curr
        s = max(0, r - xrange)
        e = -1
        for l in range(c, -1, -1):
            for j in range(s, e, -1):
                i = self.m_layout.itemAtPosition(j, l)
                w = i.widget()
                if w.isSelectable():
                    return self.setCurrentIndex(j, l)

    def goToDown(self, xrange=[1], **kwargs):
        if not self.m_curr:
            r, c = -1, 0
        else:
            r, c = self.m_curr
        e = self.m_layout.rowCount()
        s = min(r + xrange, e - 1)
        for l in range(c, self.m_layout.columnCount()):
            for j in range(s, e):
                i = self.m_layout.itemAtPosition(j, l)
                w = i.widget()
                if w.isSelectable():
                    return self.setCurrentIndex(j, l)

    def goToLeft(self, xrange=[1], **kwargs):
        if not self.m_curr:
            r, c = 0, -1
        else:
            r, c = self.m_curr
        s = max(0, c - xrange)
        e = 0
        for j in range(r, -1, -1):
            for l in range(s, e, -1):
                i = self.m_layout.itemAtPosition(j, l)
                w = i.widget()
                if w.isSelectable():
                    return self.setCurrentIndex(j, l)

    def goToRight(self, xrange=[1], **kwargs):
        if not self.m_curr:
            r, c = 0, -1
        else:
            r, c = self.m_curr
        e = self.m_layout.columnCount()
        s = min(c + xrange, e - 1)
        for j in range(r, self.m_layout.rowCount()):
            for l in range(s, e):
                i = self.m_layout.itemAtPosition(j, l)
                w = i.widget()
                if w.isSelectable():
                    return self.setCurrentIndex(j, l)

    def goToFirst(self, **kwargs):
        rows = self.m_layout.rowCount()
        columns = self.m_layout.columnCount()
        for r in range(rows):
            for c in range(columns):
                i = self.m_layout.itemAtPosition(r, c)
                w = i.widget()
                if w.isSelectable():
                    return self.setCurrentIndex(r, c)

    def goToLast(self, **kwargs):
        rows = self.m_layout.rowCount()
        columns = self.m_layout.columnCount()
        for r in range(rows - 1, -1, -1):
            for c in range(columns - 1, -1, -1):
                i = self.m_layout.itemAtPosition(r, c)
                w = i.widget()
                if w.isSelectable():
                    pos = w.position()
                    return self.setCurrentIndex(*pos)
