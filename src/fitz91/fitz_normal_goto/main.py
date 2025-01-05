from plug import Plug

class FitzNormalGoTo(Plug):

    def setup(self):
        super().setup()
        self.m_positions={}
        self.addAgent()

    def addAgent(self):
        self.app.delegman.addAgent(
                'normal', None, 'FitzView', 'goTo', self.goTo)
        self.app.delegman.addAgent(
                'normal', None, 'FitzView', 'goToState', self.goToState)

    def goToState(self, view=None, **kwargs):
        data={}
        if view:
            idx=view.currentIndex()
            item = view.item(idx)
            if item:
                pos=item.pos()
                brect = item.boundingRect()
                size = brect.translated(pos).size()
                top_left = brect.translated(pos).topLeft()
                ver=float(view.verticalScrollBar().value())
                hor=float(view.horizontalScrollBar().value())
                x = (hor -top_left.x())/size.width()
                y = (ver - top_left.y())/size.height()
                data['x'] = x 
                data['y'] = y
                data['xrange']=[idx]
        return data

    def goTo(self, view=None, kind=None, xrange=[1], **kwargs):
        if view:
            count=view.count()
            idx=view.currentIndex()
            if kind=='blockLeft':
                self.moveScreen(
                        "left", view=view, xrange=xrange, **kwargs)
            elif kind=='blockRight':
                self.moveScreen(
                        "right", view=view, xrange=xrange, **kwargs)
            elif kind=='blockUp':
                self.moveScreen(
                        "up", view=view, xrange=xrange, **kwargs)
            elif kind=='blockDown':
                self.moveScreen(
                        "down", view=view, xrange=xrange, **kwargs)
            elif kind=='down':
                self.moveLine(
                        "down", view=view, xrange=xrange, **kwargs)
            elif kind=='up':
                self.moveLine(
                        "up", view=view, xrange=xrange, **kwargs)
            elif kind=='left':
                self.moveLine(
                        "left", view=view, xrange=xrange, **kwargs)
            elif kind=='right':
                self.moveLine(
                        "right", view=view, xrange=xrange, **kwargs)
            elif kind=='next':
                idx = min(idx + xrange[-1], count)
                self.goToRange(view=view, xrange=[idx], **kwargs)
            elif kind=='prev':
                idx = max(1, idx - xrange[-1])
                self.goToRange(view=view, xrange=[idx], **kwargs)
            elif kind=='first':
                self.goToRange(view=view, xrange=[1], **kwargs)
            elif kind=='last':
                self.goToRange(view=view, xrange=[count], **kwargs)
            elif kind=='xrange' or xrange:
                self.goToRange(view=view, xrange=xrange, **kwargs)
            self.reportStateChange(view)

    def reportStateChange(self, view):
        normal=self.app.plugman.getPlug('Normal')
        if normal:
            data=self.goToState(view=view)
            normal.stateChanged.emit('goTo', view, data)

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

    def goToRange(
            self, 
            view=None, 
            xrange=[1], 
            x=0,
            y=0,
            **kwargs
            ):

        if view and xrange:
            item = view.item(xrange[-1])
            if item:
                pos=item.pos()
                brect = item.boundingRect()
                size = brect.translated(pos).size()
                top_left = brect.translated(pos).topLeft()
                hor =top_left.x() + x * size.width()
                ver =top_left.y() + y * size.height()
                view.verticalScrollBar().setValue(int(ver))
                view.horizontalScrollBar().setValue(int(hor))
                view.setCurrentIndex(xrange[-1])
                view.viewport().update()

    def restorePosition(self, view):
        state=self.goToState(view)
        if state:
            view.setVisibleItem()
            self.goToRange(view=view, **state)
