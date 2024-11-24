from PyQt6 import QtCore

from .leaf import TileLeaf


class TileLayout(QtCore.QObject):
    geometryChanged = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        self.delta = 10
        self.ratio = 1.6
        self.m_count = 0
        self.parent = parent
        self.lower_right = True
        self.root = TileLeaf()
        self.current = None
        self.previous = None
        self.previous_leaf = None
        self.current_leaf = self.root
        super().__init__(parent)

    def setSpacing(self, v):
        pass  # todo

    def setContentsMargins(self, l, t, r, b):
        pass  # todo

    def clear(self):
        for w in self.root.views():
            self.removeView(w)

    def count(self):
        return self.m_count

    def views(self):
        return self.root.views()

    def getLeaf(self, view):
        if not view:
            return
        for leaf in self.root:
            if view is leaf.view:
                return leaf

    def setLeaf(self, leaf):
        if not leaf is None:
            c, p = leaf, self.current_leaf
            (
                self.current_leaf,
                self.previous_leaf,
            ) = (c, p)

    def setView(
            self, 
            *args, 
            view=None, 
            **kwargs
            ):
        if not view is None:
            current, previous = view, self.current
            self.current, self.previous = current, previous
            leaf = self.getLeaf(view)
            self.setLeaf(leaf)
            self.update()
            return leaf

    def insertView(
            self, idx, view, horizontal=True, **kwargs):
        view.setParent(self.parent)
        if self.count() == 0:
            return self.addView(
                view, horizontal=horizontal, **kwargs
            )
        else:
            if idx == 1:
                l = self.root
            for p in self.views():
                if p.posIndex() == idx - 1:
                    l = self.getLeaf(p)
                    break
            if l:
                l.horizontal = horizontal
                l.insert(view, 1, self.ratio)
        self.update()
        self.m_count += 1
        self.setView(view)

    def addView(
        self,
        view,
        horizontal=True,
        position=None,
        **kwargs,
    ):
        view.setParent(self.parent)
        if position:
            idx, ort, p = position
            p.horizontal = ort
            p.insert(view, idx, self.ratio)
        else:
            self.current_leaf = (
                self.current_leaf or self.root
            )
            l = self.current_leaf
            l.horizontal = horizontal
            l.insert(
                view,
                int(self.lower_right),
                self.ratio,
            )
        self.m_count += 1
        if not self.current:
            self.setView(view)

    def removeView(self, v=None, **kwargs):
        v = v or self.current
        v.setManager()
        v.setParent(None)
        l = self.getLeaf(v)
        if l:
            p = l.parent
            if p:
                ort = p.horizontal
                idx = p.leaves.index(l)
                l = l.parent.remove(l)
                nv = next(l.views(), None)
                if nv is None:
                    self.current_leaf = self.root
                else:
                    self.setView(nv)
                if l.parent:
                    l.parent.update()
                else:
                    self.root.update()
                return nv, (idx, ort, p)
            l.view = None
            self.current_leaf = self.root
        self.m_count -= 1
        return None, None

    def update(self):
        r = self.parent.rect()
        x, y = r.x(), r.y()
        w, h = r.width(), r.height()
        self.root.calc_geom(x, y, w, h)
        self.geometryChanged.emit()

    def toggleSplit(self):
        if self.current_leaf.parent:
            cond = self.current_leaf.parent.horizontal
            self.current_leaf.parent.horizontal = not cond
            self.update()

    def findSibling(self, v=None, kind="next"):
        view = v or self.current_leaf.view
        views = list(self.root.views())
        i = views.index(view)
        if kind == "next":
            idx = min(len(views) - 1, i + 1)
        elif kind == "prev":
            idx = max(0, i - 1)
        if views:
            return views[idx]

    def findLeaf(self, d):
        l = self.current_leaf
        p = l.parent
        while p:
            x, y = (
                self.current_leaf.x,
                self.current_leaf.y,
            )
            w, h = (
                self.current_leaf.w,
                self.current_leaf.h,
            )
            if d == "up":
                if p.horizontal and l is p.leaves[1]:
                    n_ = p.leaves[0]
                    center = x + w * 0.5
                    while n_.view is None:
                        c = n_.leaves[1].x < center
                        if not n_.horizontal or c:
                            n_ = n_.leaves[1]
                        else:
                            n_ = n_.leaves[0]
                    return n_
            elif d == "down":
                if p.horizontal and l is p.leaves[0]:
                    n_ = p.leaves[1]
                    center = x + w * 0.5
                    while n_.view is None:
                        c = n_.leaves[1].x > center
                        if not n_.horizontal or c:
                            n_ = n_.leaves[0]
                        else:
                            n_ = n_.leaves[1]
                    return n_
            elif d == "left":
                if not p.horizontal and l is p.leaves[1]:
                    n_ = p.leaves[0]
                    center = y + h * 0.5
                    while n_.view is None:
                        c = n_.leaves[1].y < center
                        if n_.horizontal or c:
                            n_ = n_.leaves[1]
                        else:
                            n_ = n_.leaves[0]
                    return n_
            elif d == "right":
                if not p.horizontal and l is p.leaves[0]:
                    n_ = p.leaves[1]
                    center = y + h * 0.5
                    while n_.view is None:
                        c = n_.leaves[1].y > center
                        if n_.horizontal or c:
                            n_ = n_.leaves[0]
                        else:
                            n_ = n_.leaves[1]
                    return n_
            l = p
            p = l.parent

    def equalize(self):
        cond = False
        for n in self.root:
            if n.ratio != 50:
                n.ratio = 50
                cond = True
        if cond:
            self.root.equalize()
            self.update()

    def goTo(self, kind=None, xrange=None, view=None, **kwargs):
        view = view or self.current_leaf.view
        pos = ["right", "left", "down", "up"]
        if kind in pos:
            leaf = self.findLeaf(kind)
            self.setLeaf(leaf)
            return leaf
        elif kind == "next":
            next_view = self.findSibling(view, "next")
            return self.setView(view=next_view)
        elif kind == "prev":
            next_view = self.findSibling(view, "prev")
            return self.setView(view=next_view)
        elif kind == "first":
            next_view = next(self.root.views(), None)
            return self.setView(view=next_view)
        elif kind == "last":
            views = list(self.root.views())
            next_view = views[-1] if len(views) else None
            return self.setView(next_view)
        elif type(xrange) == int:
            xrange[-1] -= 1
            views = list(self.root.views())
            if 0 <= xrange < len(views):
                next_view = views[xrange]
                return self.setView(view=next_view)

    def moveTo(
        self,
        xrange=[1],
        kind=None,
        view=None,
        **kwargs,
    ):
        view = view or self.current_leaf.view
        leaf = self.getLeaf(view)
        if kind:
            l = self.findLeaf(kind)
            if l:
                self.swap(l, leaf)
            else:
                leaf = self.current_leaf
                self.removeView(leaf.view)
                newroot = TileLeaf()
                if kind in ["up", "down"]:
                    newroot.horizontal = True
                elif kind in ["left", "right"]:
                    newroot.horizontal = False
                if kind in ["up", "left"]:
                    newroot.leaves = [
                        leaf,
                        self.root,
                    ]
                elif kind in ["down", "right"]:
                    newroot.leaves = [
                        self.root,
                        leaf,
                    ]
                self.root.parent = newroot
                leaf.parent = newroot
                self.root = newroot
                leaf.view.setManager(self.parent)
                leaf.view.setParent(self.parent)
                leaf.view.activate()
        else:
            xrange = xrange or self.count()
            xrange[-1] -= 1
            views = list(self.root.views())
            if 0 <= xrange < len(views):
                v = views[xrange]
                l = self.getLeaf(v)
                self.swap(l, leaf)

    def swap(self, n=None, c=None):
        n = n or self.previous_leaf
        c = c or self.current_leaf
        cp = getattr(c, "parent", None)
        np = getattr(n, "parent", None)
        if cp and np:
            cidx = cp.leaves.index(c)
            nidx = np.leaves.index(n)
            cp.leaves[cidx] = n
            np.leaves[nidx] = c
            n.parent = cp
            c.parent = np
            self.update()
        return n, c

    def flip(self, d):
        l = self.current_leaf
        p = l.parent
        while p:
            c = not p.horizontal
            if d in ["left", "right"]:
                c = p.horizontal
            cond = c and l is p.leaves[0]
            if d in ["left", "up"]:
                cond = c and l is p.leaves[1]
            if cond:
                p.leaves = p.leaves[::-1]
                self.update()
                break
            l = p
            p = l.parent

    def resize(self, kind=None, inc=True, xrange=[1]):
        leaf = self.current_leaf
        parent = leaf.parent
        delta = self.delta * xrange[-1]
        print(kind)
        while parent:
            cond = parent.horizontal
            if kind in ["left", "right"]:
                cond = not parent.horizontal
            if kind in ["right", "down"]:
                cond = cond and leaf is parent.leaves[0]
                cond=True #todo :current:
                ratio = max(5, parent.ratio - delta)
                if inc:
                    ratio = min(95, parent.ratio + delta)
                print(cond, ratio)
            elif kind in ["left", "up"]:
                cond = cond and leaf is parent.leaves[1]
                ratio = min(95, parent.ratio + delta)
                if inc:
                    ratio = max(5, parent.ratio - delta)
            if cond:
                parent.ratio = ratio
                parent.update()
                break
            leaf = parent
            parent = leaf.parent

    def toggleFullscreen(self, v):
        if v.isFullscreen:
            o = v.app.view.overlay
            o.resized.disconnect(v.updateFullscreenPosition)
            v.setManager(v.m_prev_man)
            if self.count() == 0:
                v.m_prev_man.addView(v)
            else:
                v.m_prev_man.addView(
                    v, position=v.m_prev_pos
                )
            self.update()
            v.activate()
        else:
            m = v.manager()
            v.m_prev_man = m
            _, pos = m.removeView(v)
            v.m_prev_pos = pos
            v.app.view.overlay.addView(v)
            v.app.view.overlay.setView(v)
            v.app.view.overlay.resized.connect(
                v.updateFullscreenPosition
            )
            v.updateFullscreenPosition()
            p = getattr(v, "getPosition", None)
            if not p:
                return
            pos = p()
            v.goTo(pos[0])
        v.isFullscreen = not v.isFullscreen
