from plug import Plug

class FitzNormal(Plug):

    def setup(self):
        super().setup()
        self.m_positions={}
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        normal=self.app.plugman.getPlug('Normal')
        if normal:
            normal.addAgent('goTo', 'FitzView', self)
            self.app.buffman.viewIsDrawn.connect(self.restorePosition)

    def activate(self, kind=None, **kwargs):
        func = getattr(self, kind, None)
        if func:
            func(**kwargs)

    def blockleft(self, *args, **kwargs):
        self.moveScreen("left", *args, **kwargs)

    def blockright(self, *args, **kwargs):
        self.moveScreen("right", *args, **kwargs)

    def blockup(self, *args, **kwargs):
        self.moveScreen("up", *args, **kwargs)

    def blockdown(self, *args, **kwargs):
        self.moveScreen("down", *args, **kwargs)

    def down(self, *args, **kwargs):
        self.moveLine("down", *args, **kwargs)

    def up(self, *args, **kwargs):
        self.moveLine("up", *args, **kwargs)

    def left(self, *args, **kwargs):
        self.moveLine("left", *args, **kwargs)

    def right(self, *args,  **kwargs):
        self.moveLine("right", *args, **kwargs)

    def next(self, view=None, xrange=[1], **kwargs):
        if view:
            count=view.count()
            idx=view.currentIndex()
            idx = min(idx + xrange[-1], count)
            self.goTo(view=view, xrange=[idx])

    def prev(self, view=None, xrange=[1], **kwargs):
        if view:
            idx=view.currentIndex()
            idx = max(1, idx - xrange[-1])
            self.goTo(view=view, xrange=[idx])

    def first(self, view=None, **kwargs):
        if view:
            kwargs['xrange']=[1]
            self.goTo(view=view, **kwargs)

    def last(self, view=None, **kwargs):
        if view:
            kwargs['xrange']=[view.count()]
            self.goTo(view=view, **kwargs)

    def moveScreen(self, kind, view=None, xrange=[1], **kwargs):
        if view:
            size = view.size()
            height, width = size.height(), size.width()
            verbar = view.verticalScrollBar()
            horbar = view.horizontalScrollBar()
            height = view.m_layout.height(height)
            width = view.m_layout.height(width)
            if kind == "up":
                deltax = verbar.value() - height * xrange[-1]
                verbar.setValue(int(deltax))
            elif kind == "down":
                deltax = verbar.value() + height * xrange[-1]
                verbar.setValue(int(deltax))
            elif kind == "left":
                deltay = horbar.value() - width * xrange[-1]
                horbar.setValue(int(deltay))
            elif kind == "right":
                deltay = horbar.value() + width * xrange[-1]
                horbar.setValue(int(deltay))
            # self.positionChanged.emit()
            view.viewport().update()
            view.setVisibleItem()

    def moveLine(self, kind, view=None, xrange=[1], **kwargs):
        if view:
            size = view.size()
            height, width = size.height(), size.width()
            verbar = view.verticalScrollBar()
            horbar = view.horizontalScrollBar()
            height = view.m_layout.height(height)
            width = view.m_layout.height(width)
            height = height * view.zoomFactor  # *0.5
            width = width * view.zoomFactor  # *0.5
            if kind == "down":
                deltax = verbar.value() + height * xrange[-1]
                verbar.setValue(int(deltax))
            elif kind == "up":
                deltax = verbar.value() - height * xrange[-1]
                verbar.setValue(int(deltax))
            elif kind == "right":
                deltax = horbar.value() + width * xrange[-1]
                horbar.setValue(int(deltax))
            elif kind == "left":
                deltax = horbar.value() - width * xrange[-1]
                horbar.setValue(int(deltax))
            view.viewport().update()
            view.setVisibleItem()

    def goTo(
            self, 
            view=None, 
            xrange=[1], 
            x=0,
            y=0,
            center=False,
            **kwargs
            ):

        if view and xrange:
            xrange = xrange[-1]
            item = view.item(xrange)
            if item:
                rect = item.boundingRect()
                pos = rect.translated(item.pos())
                hor = int(pos.left() + x * pos.width())
                ver = int(pos.top() + y * pos.height())
                if center:
                    vr = view.viewport().rect()
                    ver = int(ver - vr.height() / 2.0)
                view.verticalScrollBar().setValue(ver)
                view.horizontalScrollBar().setValue(hor)
                # if center:
                #     point=QtCore.QPointF(x, y)
                #     point=item.mapToItem(point, unified=True)
                #     point=item.mapToScene(point)
                #     point=view.mapFromScene(point)
                #     view.centerOn(point.x(), point.y())
                view.viewport().update()
                view.setVisibleItem()

    def currentPosition(self, view):
        data={}
        idx=view.currentIndex()
        item = view.item(idx)
        if item:
            pos=item.pos()
            rect = item.boundingRect().translated(pos)
            top_left = view.viewport().rect().topLeft()
            top_left = view.mapToScene(top_left)
            data['x'] = (top_left.x() - rect.x()) / rect.width()
            data['y'] = (top_left.y() - rect.y()) / rect.height()
            data['xrange']=[idx]
        return data

    def restorePosition(self, view):
        position=self.currentPosition(view)
        view.setVisibleItem()
        self.goTo(view=view, **position)
