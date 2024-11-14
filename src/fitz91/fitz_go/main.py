from plug import Plug

class FitzGo(Plug):

    def setup(self):
        super().setup()
        self.m_positions={}
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        goer=self.app.plugman.plugs.get('Go')
        if goer:
            goer.addAgent('FitzView', self)

    def activate(self, kind=None, **kwargs):
        func = getattr(self, kind, None)
        if func:
            func(**kwargs)

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
            data['idx']=idx
        return data

    def goToBlockleft(self, *args, **kwargs):
        self.moveScreen("left", *args, **kwargs)

    def goToBlockright(self, *args, **kwargs):
        self.moveScreen("right", *args, **kwargs)

    def goToBlockup(self, *args, **kwargs):
        self.moveScreen("up", *args, **kwargs)

    def goToBlockdown(self, *args, **kwargs):
        self.moveScreen("down", *args, **kwargs)

    def goToDown(self, *args, **kwargs):
        self.moveLine("down", *args, **kwargs)

    def goToUp(self, *args, **kwargs):
        self.moveLine("up", *args, **kwargs)

    def goToLeft(self, *args, **kwargs):
        self.moveLine("left", *args, **kwargs)

    def goToRight(self, *args,  **kwargs):
        self.moveLine("right", *args, **kwargs)

    def goToNext(self, view=None, xrange=[1], **kwargs):
        if view:
            for i in range(xrange[0]):
                view.nextItem()

    def goToPrev(self, view=None, xrange=[1], **kwargs):
        if view:
            for i in range(xrange[0]):
                view.prevItem()

    def goToFirst(self, view=None, **kwargs):
        if view:
            kwargs['xrange']=[1]
            self.goTo(view=view, **kwargs)

    def goToLast(self, view=None, **kwargs):
        if view:
            kwargs['xrange']=[view.count()]
            self.goTo(view=view, **kwargs)

    def moveScreen(self, kind, view=None, xrange=[1]):
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

    def moveLine(self, kind, view=None, xrange=[1]):
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
                view.viewport().update()
                view.setVisibleItem()
                # self.positionChanged.emit()
