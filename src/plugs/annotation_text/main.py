from plug import Plug, tag

class Textize(Plug):

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

    @tag("<c-t>(annotate)")
    def textize(self, xrange=[1]):
        view=self.app.stateman.view()
        selector=self.app.plugman.getPlug('Selection')
        if selector:
            selection=selector.selection(view=view)
            key=xrange[0]
            color=self.m_colors.get(key, self.default_color)
            textizer=self.getAgent(view=view)
            selection['annotation_kind']='text'
            selection['annotation_color']=color
            selection['text']='text new'
            return textizer.activate(view=view, selection=selection)

    @tag("<c-T>(annotate)")
    def retextize(self, xrange=[1]):
        raise # todo
