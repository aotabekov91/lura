from PyQt6 import QtGui

from plug import Plug, tag

class Highlight(Plug):

    default_color='yellow'

    def setup(self):
        super().setup()
        self.setDefaultColor()
        self.setMapping()
        self.m_agents={}

    def setDefaultColor(self):
        rgb=QtGui.QColor(self.default_color)
        red=rgb.redF()
        green=rgb.greenF()
        blue=rgb.blueF()
        self.m_color=[red, green, blue]

    def mapping(self):
        return self.m_functions

    def setMapping(self):
        self.m_functions={}
        mapping=self.m_config.get('Mapping', {})
        for function, data in mapping.items():
            key=data.get('key', None) 
            color=data.get('color', None)
            if color:
                rgb=QtGui.QColor(color)
                red=rgb.redF()
                green=rgb.greenF()
                blue=rgb.blueF()
                color=[red, green, blue]
            else:
                color=self.m_color
            data['color']=color
            data['function']=function
            self.m_functions[key]=data

    def addAgent(self, name, annotator):
        self.m_agents[name]=annotator

    def getAgent(self, name=None, view=None):
        if view and not name:
            name=view.__class__.__name__
        return self.m_agents.get(name, None)

    @tag("<c-h>(annotate)")
    def highlight(self, xrange=[1]):
        view=self.app.stateman.view()
        selector=self.app.plugman.getPlug('Selection')
        selection=selector.selection(view)
        if selection:
            key=xrange[0]
            data=self.m_functions.get(key, {})
            color=data.get('color', self.m_color)
            agent=self.getAgent(view=view)
            selection['annotation_color']=color
            agent.activate(view=view, data=selection)
        else:
            raise # todo activate word hinting
        self.app.stateman.activate()

    @tag("<c-H>(annotate)")
    def rehighlight(self, xrange=[1]):
        raise # todo

    @tag("<c-H>(annotate)")
    def rehighlight(self, xrange=[1]):
        raise # todo
