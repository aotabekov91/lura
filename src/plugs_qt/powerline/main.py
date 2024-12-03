from plug import Plug

from .view import PowerlineWidget

class Powerline(Plug):

    def setup(self):
        super().setup()
        self.setupPowerline()
        self.connectPowerline()

    def setupPowerline(self):
        bar=self.app.view.bar
        self.m_view = None
        self.m_subview = None
        self.status = PowerlineWidget()
        bar.m_layout.insertWidget(0, self.status)
        self.status.show()

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

    def setSubview(self, v):
        m = None
        self.setKind(v)
        if v:
            m = v.model()
        self.reconnectModel()
        self.m_subview = v
        self.setModel(m)
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

    def setMode(self, m=None):
        if m:
            m = m.mode()
            m = m.title()
        self.status.setText("mode", m)

    def setSubmode(self, m=None):
        if m:
            s = self.app.stateman.submode()
            m = s.title()
        self.status.setText("submode", m)

    def setModel(self, model=None):
        if model:
            model = model.id()
        self.status.setText("model", model)

    def setDetail(self, name):
        if name:
            name = name.title()
        self.status.setText("detail", name)

    def setKeys(self, keys=None):
        self.status.setText("keys", keys)

    def setKind(self, view=None):
        if view:
            k = view.kind
            if k:
                view = k.title()
        self.status.setText("type", view)

    def setView(
            self, 
            view=None, 
            idx=None
            )->None:
        if view:
            if hasattr(view, "currentIndex"):
                c = view.currentIndex()
                if type(c) == int:
                    idx = c
            view = view.name
            self.setIndex(idx)
        self.status.setText("view", view)

    def setIndex(self, idx=None):
        if hasattr(self.m_view, "currentIndex"):
            cidx = self.m_view.currentIndex()
            if type(cidx) == int:
                idx = idx or cidx
            if hasattr(self.m_view, "count"):
                count = self.m_view.count()
                if count:
                    idx = f"{idx}/{count}"
        self.status.setText("index", idx)

    def setInfo(self, info=None):
        self.status.setText("info", info)
