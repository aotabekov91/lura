from plug import Plug, tag

class Highlight(Plug):

    default_color=(1, 0.8, 0.8)

    def setup(self):
        super().setup()
        self.setColors()
        self.m_highlighters={}

    def setColors(self):
        self.m_colors={}
        colors=self.m_config.get('Colors', {})
        for key, color in colors.items():
            key=int(key)
            color=tuple(color)
            self.m_colors[key]=color

    def addAgent(self, name, annotator):
        self.m_highlighters[name]=annotator

    def getAgent(self, name=None, view=None):
        if view and not name:
            name=view.__class__.__name__
        return self.m_highlighters.get(name, None)

    @tag(["<c-h>(annotate)", "<c-h>/<c-[>/<escape>(annotate[highlight])"])
    def toggle(self):
        view=self.app.stateman.view()
        highlighter=self.getAgent(view=view)
        if highlighter:
            self.app.stateman.toggleSubmode("highlight")

    @tag("h(annotate[highlight])")
    def highlight(self, xrange=[1]):
        view=self.app.stateman.view()
        data=view.selection()
        if data:
            key=xrange[0]
            color=self.m_colors.get(key, self.default_color)
            highlighter=self.getAgent(view=view)
            data['annotation_color']=color
            return highlighter.highlight(view=view, data=data)

    @tag("H(annotate[highlight])")
    def rehighlight(self, xrange=[1]):
        raise # todo
