from gizmo.utils import tag


class Exec:
    @tag("<escape>/<c-[>(exec)[Execlist]")
    def octivateExecMode(self):
        self.toggleExecMode()

    @tag(":(normal/exec)[Execlist]")
    def toggleExecMode(self):
        self.app.view.bar.toggleExecline()
