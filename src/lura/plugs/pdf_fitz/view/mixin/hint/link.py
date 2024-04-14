import subprocess

import fitz
from gizmo.utils import tag
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QPointF


class LinkHint:
    hasLinks = True
    canOpenLink = True
    canHintLinks = True

    def setup(self):
        super().setup()
        self.hintSelectWanted.connect(self.selectLinkHint)

    def openLink(self, l):
        k1 = fitz.LINK_GOTO
        k2 = fitz.LINK_GOTOR
        d = l["link"].dest
        if d.kind in [k1, k2]:
            raise
        elif d.kind == fitz.LINK_NAMED:
            r = self.m_model.m_data.resolve_link(d.uri)
            p, x, y = r
            tl = QPointF(x, y)
            item = self.item(p + 1)
            elem = item.element()
            tl = elem.unify(tl)
            self.goTo(p + 1, tl.x(), tl.y())
        elif d.kind == fitz.LINK_URI:
            cmd = ["qutebrowser", d.uri]
            subprocess.Popen(cmd)

    @tag("<c-l>(hint[any])[^]")
    def toggleLinkMode(self):
        sm = self.app.stateman.toggleSubmode("link")
        if sm == "link":
            self.setupHint("link")

    def selectLinkHint(self, kind, sel):
        if kind == "link":
            i = sel["link"]
            self.select(i, sel)
            self.openLink(sel)
            self.toggleHintMode()

    def getLinkHints(self):
        alist = []
        for i in self.visibleItems():
            alist += i.getLinks()
        return alist

    def paintLinkHints(self, painter, ops, widget, item):
        if self.m_hinting:
            painter.save()
            m = self.m_hint_map.get(item, {})
            pen = QtGui.QPen(
                    QtCore.Qt.GlobalColor.red, 0.0)
            painter.setPen(pen)
            for text, data in m.items():
                box = data["box"]
                rect = []
                if type(box) != list:
                    box = [box]
                for l in box:
                    rect += [item.mapToItem(l, unified=True)]
                painter.drawRects(rect)
                painter.drawText(rect[0].topLeft(), text)
            painter.restore()
