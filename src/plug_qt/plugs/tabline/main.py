from PyQt6 import QtCore, QtWidgets

from plug import Plug

from .view import TablineWidget

class Tabline(Plug):

    def setup(self):
        super().setup()
        self.m_tabs = {}
        self.setupTabline()
        self.app.appIsLaunched.connect(
                self.connectTabline)

    def setupTabline(self):
        bar=self.app.view.bar
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
            self.updateTabLabels)
        self.app.stateman.viewChanged.connect(
            self.updateTabLabels)
        self.app.stateman.viewChanged.connect(
            self.updateLabels)
        self.app.buffman.posIndexChanged.connect(
            self.updateLabels)
        self.updateTabline()

    def updateTabline(self):
        self.updateTabLabels()
        self.updateLabels()

    def clearLayout(self, layout):
        item = layout.takeAt(0)
        while not item is None:
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.hide()
            item = layout.takeAt(0)

    def searchTabber(self, view):
        if view:
            manager=view.manager()
            klass=view.__class__.__name__
            if klass=='TabView':
                return view
            return self.searchTabber(manager)

    def updateLabels(self, *args, **kwargs):
        view = self.app.stateman.view()
        if view:
            label = view.fullPosIndex()
            alabel = f"[{self.app.view.posIndex()}]"
            self.tabline.index.setText(label)
            self.tabline.andex.setText(alabel)

    def updateTabsOnCreate(self, view):
        tab=self.searchTabber(view)
        if tab:
            widget = QtWidgets.QWidget()
            layout = QtWidgets.QHBoxLayout(widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.setSpacing(5)
            widget.setLayout(layout)
            self.m_tabs[tab] = widget
            tab.currentChanged.connect(
                self.updateTabLabels)

    def updateTabLabels(self, *args, **kwargs):
        self.tabline.tabs.hide()
        view=self.app.stateman.view()
        tab=self.searchTabber(view)
        if tab:
            self.current = tab
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
                page_layout = QtWidgets.QLabel(str(name))
                page_layout.setObjectName(oname)
                page_layout.setContentsMargins(0, 0, 0, 0)
                page_layout.setAlignment(
                    QtCore.Qt.AlignmentFlag.AlignCenter
                    | QtCore.Qt.AlignmentFlag.AlignVCenter)
                flag=QtCore.Qt.AlignmentFlag
                widget_layout.addWidget(page_layout, flag.AlignCenter)
            layout.addWidget(widget)
            widget.show()
            self.tabline.tabs.show()
