from plug import Plug, tag

class TreeNormal(Plug):

    @tag('<c-i>(normal)[TreeView]')
    def test(self):
        raise

    def activate(
            self, 
            view=None, 
            action=None, 
            kind='goTo', 
            **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent, window=self.findAgent(action, view)
        if agent:
            return agent.activate(
                    window=window, 
                    kind=kind, 
                    action=action, 
                    **kwargs)
