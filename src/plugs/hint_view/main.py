from PyQt6 import QtCore, QtWidgets

from plug import tag, Plug

class ViewHint(Plug):

    view_hint_style = "color: green"

    def setup(self):
        super().setup()
        self.m_hints={}
        self.m_hint=None
        self.m_hinting=False

    def functor(self, key, earman):
        digits=self.app.earman.digits()
        if digits:
            digits=digits[-1]
            self.m_hint=digits
            if digits in self.m_hints:
                data=self.m_hints[digits]
                view=data['view']
                self.octivate()
                view.activate()
                return True
            for hint in self.m_hints:
                partial=hint[:len(digits)]
                if digits==partial:
                    self.app.view.redraw()
                    return True
        self.m_hint=''
        self.app.view.redraw()
        return True

    @tag("v(hint)")
    def toggle(self):
        submode=self.app.stateman.setSubmode(
                submode="view", toggle_submode=True)
        if submode == "view":
            self.activate()
        else:
            self.octivate()

    def activate(self):
        self.app.stateman.setFunctor(functor=self.functor)
        self.app.view.painted.connect(self.paint)
        self.app.view.update()

    def octivate(self):
        self.m_hint=None
        self.m_hinting = False
        for _, data in self.m_hints.items():
            label=data['label']
            label.hide()
            label.setParent(None)
        self.app.view.painted.disconnect(self.paint)
        self.app.stateman.activate()
        self.app.view.update()
        self.m_hints = {}

    def assignLabels(self):
        for hint, data in self.m_hints.items():
            label = QtWidgets.QLabel(
                    hint, parent=self.app.view)
            data['label']=label
            box = data["box"]
            label.setGeometry(box)
            w, h = box.width(), box.height()
            label.setAlignment(
                QtCore.Qt.AlignmentFlag.AlignCenter
            )
            s = f"font-size: {min(w, h)}px;"
            s += f"{self.view_hint_style};"
            label.setStyleSheet(s)
            label.show()

    def assignHints(self):
        views=self.getViews()
        hinter=self.app.plugman.getPlug('Hint')
        _, self.m_hints=hinter.generateHints(views, 'digits')

    def getViews(self):
        alist = []
        views = self.app.buffman.views()
        for view in views:
            if view.isVisible():
                point = QtCore.QPoint(1, 1)
                point = self.mapToUI(point, view)
                r = view.rect()
                x, y = int(point.x() - 1), int(point.y() - 1)
                w, h = r.width(), r.height()
                rect = QtCore.QRect(x, y, w, h)
                alist += [{
                    "view": view, 
                    "box": rect,
                    "pos": (x, y)
                    }]
        return sorted(alist, key=lambda d: d["pos"])

    def mapToUI(self, point, ui):
        parent = ui.parent()
        if not parent:
            return point
        current = ui.mapToParent(point)
        return self.mapToUI(current, parent)

    def paint(self, obj, e):
        if not self.m_hinting:
            self.assignHints()
            self.assignLabels()
            self.m_hinting=True
