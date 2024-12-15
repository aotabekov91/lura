from plug import Plug, tag

from .view import PowerlineWidget

class Powerline(Plug):

    def setup(self):
        super().setup()
        self.setupPowerline()
        self.connectPowerline()
        self.app.appSoonStarts.connect(self.updateStatus)

    def updateStatus(self):
        mode=self.app.stateman.mode()
        submode=self.app.stateman.submode()
        view=self.app.stateman.view()
        subview=self.app.stateman.subview()
        self.setMode(mode)
        self.setSubmode(submode)
        self.setView(view)
        self.setSubview(subview)

    def setupPowerline(self):
        bar=self.app.view.bar
        self.m_view = None
        self.m_subview = None
        self.view = PowerlineWidget()
        bar.m_layout.insertWidget(0, self.view)
        self.view.show()

    def connectPowerline(self):
        self.app.earman.keysChanged.connect(
                self.setKeys)
        self.app.stateman.modeChanged.connect(
                self.setMode)
        self.app.stateman.viewChanged.connect(
            self.updateView)
        self.app.stateman.subviewChanged.connect(
            self.setSubview)
        self.app.stateman.submodeChanged.connect(
            self.setSubmode)

    def setSubview(self, view):
        mode = None
        self.setKind(view)
        if view:
            mode = view.model()
        self.reconnectModel()
        self.m_subview = view
        self.setModel(mode)
        self.reconnectModel("connect")

    def updateView(self, view):
        self.reconnect()
        self.m_view = view
        self.setView(view)
        self.reconnect("connect")

    def reconnectModel(self, kind="disconnect"):
        if self.m_subview:
            for f in [
                "modelChanged",
            ]:
                s = getattr(self.m_subview, f, None)
                if s:
                    s = getattr(s, kind)
                    s(getattr(self, "setModel"))

    def reconnect(self, kind="disconnect"):
        if self.m_view:
            for func in [
                "indexChanged",
                "detailChanged",
            ]:
                signal = self.m_view.getAttr(func, "signal")
                name = func.replace("Changed", "")
                name = "set" + name.title()
                if signal:
                    signal = getattr(signal, kind)
                    signal(getattr(self, name))

    def setMode(self, mode=None):
        if mode:
            mode = mode.title()
        self.view.setText("mode", mode)

    def setSubmode(self, submode=None):
        if submode:
            submode = submode.title()
        self.view.setText("submode", submode)

    def setModel(self, model=None):
        if model:
            model = model.id()
        self.view.setText("model", model)

    def setDetail(self, name):
        if name:
            name = name.title()
        self.view.setText("detail", name)

    def setKeys(self, keys=None):
        self.view.setText("keys", keys)

    def setKind(self, view=None):
        if view:
            view = view.kind
        self.view.setText("type", view)

    def setView(
            self, 
            view=None, 
            idx=None
            )->None:
        if view:
            if hasattr(view, "currentIndex"):
                cidx = view.currentIndex()
                if type(cidx) == int:
                    idx = cidx
            view = view.name
            self.setIndex(idx)
        self.view.setText("view", view)

    def setIndex(self, idx=None):
        if hasattr(self.m_view, "currentIndex"):
            cidx = self.m_view.currentIndex()
            if type(cidx) in [int, str]:
                idx = idx or cidx
            elif type(idx)==int:
                idx+=1
            elif idx and idx.isValid():
                idx=cidx.row()+1
            if hasattr(self.m_view, "count"):
                count = self.m_view.count()
                if idx and count:
                    idx = f"{idx}/{count}"
        self.view.setText("index", idx)

    def setInfo(self, info=None):
        self.view.setText("info", info)

    @tag('tp')
    def toggle(self):
        self.view.toggle()
