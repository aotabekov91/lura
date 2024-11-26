from plug import Plug, tag

class Highlight(Plug):

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

    @tag("<c-h>(annotate/visual[any])")
    def highlight(self, xrange=[1]):
        view=self.app.stateman.view()
        selector=self.app.plugman.getPlug('Selection')
        selection=selector.selection(view)
        if selection:
            key=xrange[0]
            color=self.m_colors.get(key, self.default_color)
            agent=self.getAgent(view=view)
            selection['annotation_color']=color
            agent.activate(view=view, data=selection)
        else:
            raise # todo activate word hinting
        self.app.stateman.toggle()

    @tag("<c-H>(annotate)")
    def rehighlight(self, xrange=[1]):
        raise # todo

    @tag("<c-H>(annotate)")
    def rehighlight(self, xrange=[1]):
        raise # todo
