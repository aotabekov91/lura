from plug import Plug, tag

class Exec(Plug):

    @tag([":(normal)", "<escape>/<c-[>(exec)"])
    def toggle(self):
        self.app.view.bar.toggleEdit()
        self.app.stateman.toggle('exec')
