from fitz import LINK_GOTO 
from PyQt5 import QtCore

class Links:

    hasLinks=True

    def setup(self):

        super().setup()
        self.m_links=[]
        self.m_links_set=False

    def setLinks(self):

        self.m_links_set=True
        l=self.m_data.first_link
        while l:
            data={}
            data['link']=l
            data['box']=self.createRect(l.rect)
            self.m_links+=[data]
            l=l.next

    def createRect(self, r):

        tl = QtCore.QPointF(r.x0, r.y0)
        br = QtCore.QPointF(r.x1, r.y1)
        r=QtCore.QRectF(tl, br)
        return self.m_norm_inv.mapRect(r)

    def getLinks(self):

        if not self.m_links_set:
            self.setLinks()
        return self.m_links
