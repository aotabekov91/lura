from plug.utils import tag


class Exec:
    #todo
    @tag("<escape>/<c-[>(exec)")
    def octivateExecMode(self):
        self.toggleExecMode()
        self.app.stateman.toggle('normal')

    @tag(":(normal)")
    def toggleExecMode(self):
        self.app.ui.bar.toggleEdit()
        self.app.stateman.toggle('exec')
