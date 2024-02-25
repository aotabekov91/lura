from gizmo.plug.utils import tag


class BoxVisual:
    canVisualizeBoxes = True

    def setup(self):
        super().setup()
        self.hintSelectWanted.connect(self.visualBoxSelect)

    @tag("<c-i>", modes=["visual[box]|^own"])
    def incrementVisualBoxScale(self, rstart=1):
        self.m_visual_boxes = None
        self.m_hint_capturing = True
        self.setupHint(
            inc=True,
            rstart=rstart,
            kind="visualbox",
        )

    @tag("<c-o>", modes=["visual[box]|^own"])
    def decrementVisualBoxScale(self, rstart=1):
        self.m_visual_boxes = None
        self.m_hint_capturing = True
        self.setupHint(
            inc=False,
            rstart=rstart,
            kind="visualbox",
        )

    @tag("<c-b>", modes=["visual[any]|^own"])
    def toggleVisualBoxMode(self):
        if self.checkProp("canHintBoxes"):
            self.app.moder.toggleSubmode("box")

    @tag("<c-f>", modes=["visual[box]|^own"])
    def hintVisualBoxMode(self):
        self.m_visual_boxes = None
        self.setupHint(kind="visualbox")

    @tag("<c-j>", modes=["visual[box]|^own"])
    def visualBoxJumpTo(self):
        self.setupHint(kind="box")

    @tag("o", modes=["visual[box]|^own"])
    def visualBoxGoToFirst(self):
        self.visualBoxGoTo(kind="first")

    @tag("$", modes=["visual[box]|^own"])
    def visualBoxGoToEnd(self):
        self.visualBoxGoTo(kind="last")

    @tag("k", modes=["visual[box]|^own"])
    def visualBoxGoToUp(self, rstart=1):
        self.visualBoxGoTo("up", rstart=rstart)

    @tag("j", modes=["visual[box]|^own"])
    def visualBoxGoToDown(self, rstart=1):
        self.visualBoxGoTo("down", rstart=rstart)

    @tag("l", modes=["visual[box]|^own"])
    def visualBoxGoToLeft(self, rstart=1):
        self.visualBoxGoTo("right", rstart=rstart)

    @tag("h", modes=["visual[box]|^own"])
    def visualBoxGoToRight(self, rstart=1):
        self.visualBoxGoTo("left", rstart=rstart)

    def visualBoxGoTo(self, kind, rstart=1):
        for i in range(rstart):
            s = self.m_visual_box
            if not s:
                return
            p = s["pos"]
            r, c = p[0], p[1]
            if kind == "down":
                r += 1
            elif kind == "up":
                r -= 1
            elif kind == "right":
                c += 1
            elif kind == "left":
                c -= 1
            else:
                return
            n = self.m_visual_poses.get((r, c))
            if n:
                c = n["isSelected"]
                self.m_visual_box = n
                n["isSelected"] = not c
                self.updateHintItems()

    @tag("<c-s>", modes=["visual[box]|^own"])
    def selectVisualboxHints(self):
        box = []
        sel = {"box": box}
        for b in self.m_visual_boxes:
            if b.get("isSelected"):
                box += b.get("box")
                sel["item"] = b.get("item")
        i = sel.get("item")
        self.m_visual_boxes = []
        self.cleanUpHinting()
        self.app.moder.toggle()
        self.select(i, sel)

    def getVisualboxHints(self, rstart=1, inc=None):
        alist = self.getBoxHints(rstart, inc)
        if self.m_visual_boxes != alist:
            self.m_visual_poses = {}
            self.m_visual_boxes = alist
            for a in alist:
                p = a["pos"]
                a["isSelected"] = False
                self.m_visual_poses[p] = a
            p = (0, 0)
            c = self.m_visual_poses[p]
            self.m_visual_box = c
            return alist
        return self.m_visual_boxes

    def visualBoxSelect(self, kind, sel):
        m = self.app.moder.mode()
        sm = self.app.moder.submode()
        if m == "visual" and sm == "box":
            c = sel["isSelected"]
            sel["isSelected"] = not c

    def updateVisualHint(self, key):
        m = self.app.moder.mode()
        sm = self.app.moder.submode()
        if not (m == "visual" and sm == "box"):
            self.updateHint(key)
        else:
            match = self.getHintMatches(key)
            if len(match) == 1:
                d = match[list(match.keys())[0]]
                c = d["isSelected"]
                d["isSelected"] = not c
                self.m_visual_box = d
                self.m_hint_key = ""
                self.updateHintItems()
                self.m_hint_capturing = False
