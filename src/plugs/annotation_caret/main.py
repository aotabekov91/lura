from plug import Plug, tag

class Caretize(Plug):

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

    @tag("<c-c>(annotate)")
    def caretize(self, xrange=[1]):
        view=self.app.stateman.view()
        selector=self.app.plugman.plugs.get('Selection')
        selection=selector.selection(view)
        if selection:
            key=xrange[0]
            color=self.m_colors.get(key, self.default_color)
            caretizer=self.getAgent(view=view)
            selection['annotation_color']=color
            return caretizer.activate(view=view, data=selection)

    @tag("<c-C>(annotate)")
    def recaretize(self, xrange=[1]):
        raise # todo
