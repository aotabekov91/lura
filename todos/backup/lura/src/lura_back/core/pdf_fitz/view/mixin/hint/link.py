import math
import fitz
import subprocess

from gizmo.utils import tag
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QPointF


class LinkHint:
    hasLinks = True
    canOpenLink = True
    canHintLinks = True

    def setup(self):
        super().setup()
        self.hintSelectWanted.connect(
                self.selectLinkHint)

    def openLink(self, link):
        if not link: return
        d = link["link"].dest
        if d.kind in [fitz.LINK_GOTO, fitz.LINK_GOTOR]:
            raise
        elif d.kind in [fitz.LINK_URI]:
            cmd = ["qutebrowser", d.uri]
            subprocess.Popen(cmd)
        elif d.kind in [fitz.LINK_NAMED, fitz.LINK_LAUNCH]:
            r = self.m_model.m_data.resolve_link(d.uri)
            p, x, y = r
            if math.isnan(x): x=0.
            if math.isnan(y): y=0.
            tl = QPointF(x, y)
            item = self.item(p + 1)
            elem = item.element()
            tl = elem.unify(tl)
            self.goTo(p + 1, tl.x(), tl.y())

    @tag("<c-l>(hint[any])[^]")
    def toggleLinkMode(self):
        sm = self.app.stateman.toggleSubmode("link")
        if sm == "link":
            self.setupHint("link")

    def selectLinkHint(self, kind, sel):
        if kind == "link":
            try:
                self.openLink(sel)
            except:
                pass
            self.app.stateman.toggle()

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
                painter.drawText(rect[0].topLeft(), text)
            painter.restore()
