from lura.gizmo.utils import tag


class Command:
    @tag("<c-,>(normal/command)")
    def toggleCommandMode(self):
        return self.app.stateman.toggle(
            delisten=True,
            mode="command",
            exit_mode="normal",
        )

    @tag("<escape>/<c-[>(command)")
    def octivateCommandMode(self):
        m = self.app.stateman.mode()
        if m == "command":
            self.app.stateman.toggle()
