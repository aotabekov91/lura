from PyQt6 import QtCore

from plug_qt import vimo, widget
from plug.utils import tag


class TabView(
    vimo.View,
    widget.StackedWidget,
):
    hasTabs = True
    current = None
    previous = None
    tab_classes = {}
    canSetView = True
    initial_create = True
    prefix_keys = ["<c-t>(normal)"]
    viewAdded = QtCore.pyqtSignal(object)
    viewCreated = QtCore.pyqtSignal(object)

    def updateKlass(self):
        super().updateKlass()
        pos = self.m_kwargs.get("tab_classes", {}).copy()
        if pos:
            self.tab_classes.update(pos)

    def child(self, pos, recursive=True):
        if pos.startswith("x") and self.current:
            i = self.current.posIndex()
            pos = pos.replace("x", str(i), 1)
        elif pos.startswith("-1"):
            i = self.count() - 1
            pos = pos.replace("-1", str(i), 1)
        return super().child(pos, recursive)

    @tag("n(normal)")
    def addAndGoToNewTab(self, focus=False, **kwargs):
        return self.addNewTab(focus=True, **kwargs)

    @tag("N(normal)")
    def addNewTab(self, focus=False, **kwargs):
        t = self.getNewTab(**kwargs)
        if focus and t:
            self.setView(t)
            t.activate()
        return t

    @tag("T(normal)")
    def addCopyTab(self, tab=None, **kwargs):
        c = self.getCopyTab(tab, **kwargs)
        if c:
            self.addView(c)
        return c

    @tag("t(normal)")
    def addAndGoToCopyTab(self, tab=None, **kwargs):
        c = self.addCopyTab(tab, **kwargs)
        if c:
            c.activate()
        return c

    @tag("c(normal)[^]")
    def closeCurrentTab(self):
        return self.tabClose()

    @tag("x(normal)[^]")
    def swapCurrent(self, **kwargs):
        self.setView(self.previous)

    @tag("l(normal)[^]")
    def tabGoToNext(self):
        self.tabGoTo(kind="next")

    @tag("h(normal)[^]")
    def tabGoToPrev(self):
        self.tabGoTo(kind="prev")

    @tag("H(normal)[^]")
    def tabMoveToLeft(self):
        self.tabMoveTo(kind="prev")

    @tag("L(normal)[^]")
    def tabMoveToRight(self):
        self.tabMoveTo(kind="next")

    @tag("~gt(normal)")
    def tabGoTo(self, xrange=[], kind=None):
        idx = self.currentIndex()
        if kind == "prev":
            xrange[-1] = max(0, idx - 1)
        elif kind == "next":
            xrange[-1] = idx + 1
            if xrange[-1] >= self.count():
                xrange[-1] = 0
            # xrange=min(self.count()-1, idx+1)
        elif kind == "first":
            xrange[-1] = 0
        elif kind == "last":
            xrange[-1] = self.count() - 1
        elif xrange is None:
            xrange[-1] = self.count() - 1
        elif not xrange:
            return
        else:
            xrange[-1] -= 1
        ntab = self.widget(xrange[-1])
        if ntab:
            ntab.activate()

    @tag("~gT(normal)[^]")
    def tabMoveTo(self, kind=None, xrange=None):
        c = self.currentIndex()
        if kind == "prev":
            xrange = max(0, c - 1)
        elif kind == "next":
            xrange = min(self.count() - 1, c + 1)
        elif type(xrange) == int:
            xrange[-1] -= 1
        elif xrange is None:
            xrange = self.count() - 1
        else:
            return
        w = self.widget(c)
        self.removeView(w)
        self.insertView(xrange, w)
        self.setView(w)

    def initiate(self):
        view = self.addNewTab()
        if view:
            self.setView(view=view, focus=False)

    def setup(self):
        super().setup()
        if self.initial_create:
            self.initiate()

    def getCopyTab(self, tab=None, **kwargs):
        c = tab or self.current
        if c and self.checkProp("canCopy", c):
            copy = c.copy()
            self.viewCreated.emit(copy)
            return copy

    def getNewTab(self, **kwargs):
        n = self.tabGet()
        if n:
            self.addView(n, **kwargs)
        return n

    def addView(self, view, **kwargs):
        self.tabAdd(view, **kwargs)
        view.setManager(self)
        view.hasTabber = True
        view.m_tabber = self
        self.viewAdded.emit(view)
        self.tabReindex()
        return view

    def setView(
        self,
        *args,
        view=None,
        recursive_activate=False,
        **kwargs,
    ):
        if view:
            current, previous = view, self.current
            self.current, self.previous = current, previous
            self.setCurrentIndex(view.posIndex() - 1)
            if not self.activated and recursive_activate:
                self.activate(
                    recursive_activate=True,
                    **kwargs,
                )

    def tabGet(self, kind="default"):
        k = self.tab_classes.get(kind)
        if k:
            v = k(
                parent=self,
                app=self.app,
                pindex=self.m_id,
                config=self.m_config,
            )
            self.viewCreated.emit(v)
            return v

    def tabAdd(self, tab, **kwargs):
        tab.m_tabber = self
        idx = self.addWidget(tab)
        tab.setPosIndex(idx + 1)
        tab.m_tab_name = idx

    def insertView(
        self,
        idx=-1,
        view=None,
        **kwargs,
    ):
        idx += 1
        super().insertWidget(idx, view)
        view.setPosIndex(idx)
        view.setManager(self)
        view.m_tab_name = idx
        view.hasTabber = True
        view.m_tabber = self
        self.viewAdded.emit(view)
        self.tabReindex()
        return view

    def removeView(self, v, **kwargs):
        super().removeWidget(v)
        idx = v.posIndex()
        self.tabReindex()
        v.setManager()
        v.setPosIndex()
        return v, idx

    def tabReindex(self):
        for i in range(self.count()):
            v = self.widget(i)
            v.setPosIndex(i + 1)

    def tabClose(self, tab=None, limit=1):
        if self.count() <= limit:
            return
        tab = tab or self.current
        if tab:
            idx = tab.posIndex()
            tab.m_tabber = None
            self.removeView(tab)
            delattr(tab, "m_tabber")
        tab = self.widget(idx - 1)
        if tab:
            self.setView(tab)

    def activate(self, descend=True, **kwargs):
        super().activate(**kwargs)
        if self.current and descend:
            self.current.activate()
