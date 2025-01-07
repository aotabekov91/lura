from plug import Plug, tag

class AnnotationHint(Plug):

    def setup(self):
        super().setup()
        self.addAgent()

    def addAgent(self):
        self.app.delegman.addAgent(
                mode='hint', 
                submode='annotation', 
                action='activate', 
                functor=self.activate)
        self.app.delegman.addAgent(
                mode='hint', 
                submode='annotation', 
                action='octivate', 
                functor=self.octivate)

    @tag("<c-a>(hint)")
    def activate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        agent=self.app.delegman.getAgent(
                'hint', 'annotation', view, delegate='view')
        if agent:
            super().activate()
            self.app.stateman.setSubmode(
                    submode="annotation", submoder=self)
            self.app.delegman.delegate(
                    'hint', 'annotation', view, 'activate', data=kwargs) 

    @tag("<c-a>/<c-[>/<escape>(hint[annotation])")
    def octivate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        super().octivate()
        self.app.stateman.setSubmode()
        self.app.delegman.delegate(
                'hint', 'annotation', view, 'octivate', data=kwargs) 
