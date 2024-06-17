from lura.gizmo.utils import tag


class Node:
    def __init__(self, d=None, n=None, p=None):
        self.d = d
        self.n = n
        self.p = p


class Leaper:
    hasLeaper = True
    node_class = Node

    def setup(self):
        super().setup()
        self.setupLeaper()

    def setupLeaper(self):
        if self.checkProp("canLocate"):
            self.m_leap_node = self.node_class()
            self.reconnectLeaper()

    def getLeapData(self):
        return self.getLocator(kind="position")

    def setLeapNode(self):
        d = self.getLeapData()
        c = self.m_leap_node
        c.n = self.node_class(p=c, d=d)
        self.m_leap_node = c.n

    def reconnectLeaper(self, kind="connect"):
        if kind == "connect":
            self.positionJumped.connect(self.setLeapNode)
        else:
            self.positionJumped.disconnect(self.setLeapNode)

    def leaperGoTo(self, xrange=[1], leap="next", **kwargs):
        for i in range(xrange):
            c = self.m_leap_node
            if leap == "next" and c.n:
                self.m_leap_node = c.n
                self.openLocator(
                    data=c.n.d, kind="position"
                )
            elif leap == "prev" and c.p and c.p.d:
                self.m_leap_node = c.p
                self.openLocator(
                    data=c.p.d, kind="position"
                )

    def leaperGoToNext(self, **kwargs):
        self.reconnectLeaper("disconnect")
        self.leaperGoTo(leap="next", **kwargs)
        self.reconnectLeaper()

    def leaperGoToPrev(self, xrange=[1], **kwargs):
        self.reconnectLeaper("disconnect")
        self.leaperGoTo(leap="prev", **kwargs)
        self.reconnectLeaper()
