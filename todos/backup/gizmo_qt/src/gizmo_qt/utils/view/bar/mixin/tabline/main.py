from PyQt6 import QtCore, QtWidgets

from gizmo.utils import tag

from .widget import TablineWidget


class Tabline:
    def setupUI(self):
        super().setupUI()
        self.setupTabline()
        self.app.appIsLaunched.connect(self.connectTabline)
        self.app.appIsLaunched.connect(self.updateTabline)

    def updateTabline(self):
        self.updateTabLabels()
        self.updateLabels()

    def updateLabels(self, *args, **kwargs):
        v = self.app.stateman.view()
        if v:
            label = v.fullPosIndex()
            alabel = f"[{self.app.view.posIndex()}]"
            self.tabline.index.setText(label)
            self.tabline.andex.setText(alabel)

    def setupTabline(self):
        self.m_tabs = {}
        self.rename_widget = None
        self.tabline = TablineWidget()
        idx = self.stack.addWidget(self.tabline)
        self.tabline.m_idx = idx
        self.stack.setCurrentIndex(idx)
        self.tabline.show()
        self.stack.show()

    def connectTabline(self):
        self.app.buffman.viewCreated.connect(
            self.updateTabs
        )
        self.app.stateman.viewChanged.connect(
            self.updateTabLabels
        )
        self.app.stateman.viewChanged.connect(
            self.updateLabels
        )
        self.app.buffman.posIndexChanged.connect(
            self.updateLabels
        )

    @tag("r(command)")
    def startRenameTab(self, xrange=None):
        if self.current:
            idx = self.current.currentIndex()
            if xrange:
                idx = xrange[-1] - 1
            self.activate()
            self.setSubmode("rename")
            w = self.current.widget(idx)
            self.rename_widget = w
            self.activeEdit(edit=w.m_tab_name)

    @tag("<enter>/<return>")
    def renameTab(self):
        w = self.rename_widget
        if self.current and w:
            n = self.app.view.bar.edit.text()
            w.m_tab_name = n
            self.updateTabLabels(tab=self.current)
        self.octivateEdit()

    def clearLayout(self, l):
        i = l.takeAt(0)
        while not i is None:
            w = i.widget()
            if w:
                w.setParent(None)
                w.hide()
            i = l.takeAt(0)

    def updateTabIndexLabel(self, idx):
        self.updateTabLabels(tab=self.current)

    def updateTabLabels(self, view=None, tab=None):
        if hasattr(view, "hasTabs"):
            tab = view
        if not tab:
            t = getattr(view, "m_tabber", None)
        self.current = t
        if not t:
            return
        ll = self.tabline.tabs.layout()
        self.clearLayout(ll)
        self.tabline.tabs.hide()
        tw = self.m_tabs.get(t)
        if not tw:
            self.updateTabs(t)
        tw = self.m_tabs.get(t)
        tl = tw.layout()
        idx = t.currentIndex()
        self.clearLayout(tl)
        for i in range(t.count()):
            oname = "Tab"
            w = t.widget(i)
            widx = w.posIndex()
            idx = w.identifier()
            name = f"[{widx}]"
            if idx:
                name = f"{idx} {name}"
            if t.current == w:
                name = f"{name}*"
                oname = "CurrentTab"
            l = QtWidgets.QLabel(str(name))
            l.setObjectName(oname)
            l.setContentsMargins(0, 0, 0, 0)
            l.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignCenter
                | QtCore.Qt.AlignmentFlag.AlignVCenter
            )
            tl.addWidget(
                l, QtCore.Qt.AlignmentFlag.AlignCenter
            )
        ll.addWidget(tw)
        tw.show()
        self.tabline.tabs.show()

    def updateTabs(self, v):
        t = None
        if self.checkProp("hasTabs", v):
            t = v
        elif self.checkProp("m_tabber", v):
            t = v.m_tabber
        if t:
            w = QtWidgets.QWidget()
            l = QtWidgets.QHBoxLayout(w)
            l.setContentsMargins(0, 0, 0, 0)
            l.setSpacing(5)
            w.setLayout(l)
            self.m_tabs[t] = w
            t.currentChanged.connect(
                self.updateTabIndexLabel
            )
