from plug import Plug, tag

class Underline(Plug):

    default_color=(1, 0.8, 0.8)

    def setup(self):
        super().setup()
        self.setColors()
        self.m_agents={}

    def setColors(self):
        self.m_colors={}
        colors=self.m_config.get('Colors', {})
        for key, color in colors.items():
            key=int(key)
            color=tuple(color)
            self.m_colors[key]=color

    def addAgent(self, name, annotator):
        self.m_agents[name]=annotator

    def getAgent(self, name=None, view=None):
        if view and not name:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    @tag("<c-u>(annotate)")
    def underline(self, xrange=[1]):
        view=self.app.stateman.view()
        selector=self.app.plugman.getPlug('Selection')
        selection=selector.selection(view)
        if selection:
            key=xrange[0]
            color=self.m_colors.get(key, self.default_color)
            underliner=self.getAgent(view=view)
            selection['annotation_color']=color
            return underliner.activate(view=view, data=selection)

    @tag("<c-U>(annotate)")
    def reunderline(self, xrange=[1]):
        raise # todo
