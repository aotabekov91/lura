from PyQt6 import QtCore


class ZXYPos:

    positionChanged = QtCore.pyqtSignal()
    positionJumped = QtCore.pyqtSignal(
            object, object)
    positionToBeJumped = QtCore.pyqtSignal(
            object, object)

    # def setup(self):
    #     super().setup()
    #     self.m_position = None
    #     # self.viewIsToBeRedrawn.connect(self.savePosition)
    #     self.viewIsRedrawn.connect(self.jumpToPosition)
    #     # self.positionChanged.connect(self.savePositionState)

    # def getPosition(self, data=None, kind=None):
    #     i = self.item(self.m_curr)
    #     if i:
    #         r = i.boundingRect().translated(i.pos())
    #         tl = self.viewport().rect().topLeft()
    #         tl = self.mapToScene(tl)
    #         x = (tl.x() - r.x()) / r.width()
    #         y = (tl.y() - r.y()) / r.height()
    #         return self.m_curr, x, y
    #     return 1, 0, 0

    # def goTo(
    #     self,
    #     xrange=[1],
    #     x=0,
    #     y=0,
    #     center=False,
    #     **kwargs,
    # ):
    #     # position=self.getPositionLocator()
    #     # self.positionToBeJumped.emit(self, position)
    #     if not xrange:
    #         self.goToLast()
    #     if type(xrange) == list:
    #         xrange = xrange[0]
    #     self.jumpToPosition(
    #         center=center,
    #         pos=(xrange, x, y),
    #     )
    #     # position=self.getPositionLocator()
    #     # self.positionJumped.emit(self, position)
    #     self.positionChanged.emit()

    # def jumpToPosition(
    #     self,
    #     pos=None,
    #     center=False,
    # ):
    #     pos = pos or self.m_position
    #     if pos:
    #         self.updatePosition(*pos, center=center)
    #         self.viewport().update()
    #         self.setVisibleItem()

    # def updatePosition(
    #     self,
    #     xrange=[1],
    #     x=0,
    #     y=0,
    #     center=False,
    # ):
    #     item = self.item(xrange)
    #     if item:
    #         r = item.boundingRect()
    #         p = r.translated(item.pos())
    #         h = int(p.left() + x * p.width())
    #         v = int(p.top() + y * p.height())
    #         if center:
    #             vr = self.viewport().rect()
    #             v = int(v - vr.height() / 2.0)
    #         self.verticalScrollBar().setValue(v)
    #         self.horizontalScrollBar().setValue(h)

    # def getBarPosition(self, d, x, y):
    #     item = self.item(d)
    #     if item:
    #         rect = item.boundingRect()
    #         pos = rect.translated(item.pos())
    #         height = int(pos.left() + x * pos.width())
    #         width = int(pos.top() + y * pos.height())
    #         return height, width

    # def savePosition(self):
    #     self.m_position = self.getPosition()

    # def openPositionLocator(self, data={}, **kwargs):
    #     p = data.get("position", None)
    #     i, x, y = self.parsePositionLocator(p)
    #     self.goTo(i, x, y, **kwargs)
    #     return i, x, y

    # def getPositionLocator(self, data={}, **kwargs):
    #     kwargs["kind"] = "uniq"
    #     data = self.getLocator(data, **kwargs)
    #     i, x, y = self.getPosition()
    #     i = str(i)[:10]
    #     x = str(x)[:10]
    #     y = str(y)[:10]
    #     data["position"] = ":".join([i, x, y])
    #     return self.createLocator(data, **kwargs)

    # def setPositionLocator(self, data={}, **kwargs):
    #     i, x, y = self.openPositionLocator(data)
    #     self.setCurrentIndex(i)

    # def parsePositionLocator(self, data=None):
    #     if data:
    #         t = data.split(":")
    #         i = int(t[0])
    #         x = float(t[1])
    #         y = float(t[2])
    #         return i, x, y

    # # def savePositionState(self):
    # #     if self.checkProp("hasStates", self.m_model):
    # #         p = self.getLocator(kind="position")
    # #         p["state"] = "position"
    # #         p["value"] = p["position"]
    # #         self.m_model.addState(p)
