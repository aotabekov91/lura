from plug import Plug, tag

class Command(Plug):

    @tag(["<c-,>(normal/command)", "<escape>/<c-[>(command)"])
    def toggle(self):
        return self.app.stateman.activate(
            delisten=True,
            mode="command",
            toggle_mode=True,
            )
