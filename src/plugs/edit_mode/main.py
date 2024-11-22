from plug import Plug, tag

class EditMode(Plug):

    @tag('<escape>/<c-[>(edit)')
    def octivate(self, view=None, **kwargs):
        self.app.stateman.activate('normal')

    @tag('<c-e>(normal)')
    def activate(self, view=None, **kwargs):
        self.app.stateman.activate('edit')
