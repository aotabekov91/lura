from plug import Plug, tag


class Command(Plug):

    @tag(["<c-,>(normal/command)", "<escape>/<c-[>(command)"])
    def toggle(self):
        return self.app.stateman.toggle(
            delisten=True,
            mode="command",
            exit_mode="normal")
