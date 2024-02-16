import fitz
import subprocess
from gizmo.utils import tag
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QPointF

class LinkHint:
    
    hasLinks=True
    canOpenLink=True
    canHintLinks=True

    def setup(self):

        super().setup()
        self.hintSelectWanted.connect(
                self.selectLinkHint)

    def openLink(self, l):

        k1=fitz.LINK_GOTO
        k2=fitz.LINK_GOTOR
        d=l['link'].dest
        if d.kind in [k1, k2]:
            raise
        elif d.kind==fitz.LINK_NAMED:
            r=self.m_model.m_data.resolve_link(
                    d.uri)
            p, x, y = r
            tl=QPointF(x, y)
            item=self.item(p+1)
            elem=item.element()
            tl=elem.unify(tl)
            self.goTo(p+1, tl.x(), tl.y())
        elif d.kind==fitz.LINK_URI:
            cmd=['qutebrowser', d.uri]
            subprocess.Popen(cmd)

    @tag('<c-l>', modes=['hint[any]|^own'])
    def toggleLinkMode(self):

        sm=self.app.ui.moder.toggleSubmode('link')
        if sm=='link': 
            self.setupHint('link')

    def selectLinkHint(self, kind, sel):

        if kind=='link':
            i=sel['link']
            self.select(i, sel)
            self.openLink(sel)
            self.toggleHintMode()

    def getLinkHints(self):

        alist=[]
        for i in self.visibleItems():
            alist+=i.getLinks()
        return alist

    def paintLinkHints(self, p, o, w, i):

        if self.m_hinting:
            p.save()
            pen=QtGui.QPen(QtCore.Qt.red, 0.0)
            p.setPen(pen)
            m=self.m_hint_map.get(i, {})
            for j, d in m.items():
                b=d['box']
                tr=[]
                if type(b)!=list: b=[b]
                for l in b:
                    tr+=[i.mapToItem(l, unified=True)]
                p.drawRects(tr)
                p.drawText(tr[0].topLeft(), j)
            p.restore()
