from PyQt6 import QtCore, QtWidgets

from plug import Plug

from .view import TablineWidget

class Tabline(Plug):

    def setup(self):
        super().setup()
        self.setupTabline()
        self.app.appIsLaunched.connect(
                self.connectTabline)
        self.app.appIsLaunched.connect(
                self.updateTabline)

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
        bar=self.app.view.bar
        self.m_tabs = {}
        self.rename_widget = None
        self.tabline = TablineWidget()
        idx = bar.stack.addWidget(self.tabline)
        self.tabline.m_idx = idx
        bar.stack.setCurrentIndex(idx)
        self.tabline.show()
        bar.stack.show()

    def connectTabline(self):
        self.app.buffman.viewCreated.connect(
            self.updateTabsOnCreate)
        self.app.buffman.viewClosed.connect(
            self.updateTabsOnClose)
        self.app.stateman.viewChanged.connect(
            self.updateTabLabels)
        self.app.stateman.viewChanged.connect(
            self.updateLabels)
        self.app.buffman.posIndexChanged.connect(
            self.updateLabels)

    def updateTabsOnClose(self, view):
        manager=view.manager()
        self.updateTabLabels(view=view)

    def clearLayout(self, layout):
        item = layout.takeAt(0)
        while not item is None:
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.hide()
            item = layout.takeAt(0)

    def updateTabIndexLabel(self, *args, **kwargs):
        self.updateTabLabels(tab=self.current)

    def updateTabLabels(self, view=None, tab=None):
        if view and hasattr(view, "hasTabs"):
            tab = view
        if not tab:
            tab = getattr(view, "m_tabber", None)
        self.current = tab
        if not tab:
            return
        if not tab.hasTabs:
            return
        layout = self.tabline.tabs.layout()
        self.clearLayout(layout)
        self.tabline.tabs.hide()
        widget = self.m_tabs.get(tab)
        if not widget:
            self.updateTabsOnCreate(tab)
        widget = self.m_tabs.get(tab)
        widget_layout = widget.layout()
        idx = tab.currentIndex()
        self.clearLayout(widget_layout)
        for page in range(tab.count()):
            oname = "Tab"
            w = tab.widget(page)
            widx = w.posIndex()
            idx = w.identifier()
            name = f"[{widx}]"
            if idx:
                name = f"{idx} {name}"
            if tab.current == w:
                name = f"{name}*"
                oname = "CurrentTab"
            l = QtWidgets.QLabel(str(name))
            l.setObjectName(oname)
            l.setContentsMargins(0, 0, 0, 0)
            l.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignCenter
                | QtCore.Qt.AlignmentFlag.AlignVCenter)
            widget_layout.addWidget(l, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(widget)
        widget.show()
        self.tabline.tabs.show()

    def updateTabsOnCreate(self, view):
        tab = None
        if not view:
            return
        if view.checkProp("hasTabs", view):
            tab = view
        elif view.checkProp("m_tabber", view):
            tab = view.m_tabber
        if tab:
            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(5)
            widget.setLayout(layout)
            self.m_tabs[tab] = widget
            tab.currentChanged.connect(
                self.updateTabIndexLabel)
