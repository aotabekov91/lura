from plug import Plug, tag

class Edit(Plug):

    @tag(['<c-e>(normal/edit)', '<escape>/<c-[>(edit)'])
    def toggle(self, **kwargs):
        self.app.stateman.toggle('edit')
