from plug import Plug, tag, deleg

class AnnotationHint(Plug):

    @deleg('activate@(hint[annotation])')
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
                    mode='hint', 
                    submode='annotation', 
                    view=view, 
                    action='activate', 
                    data=kwargs) 

    @deleg('octivate@(hint[annotation])')
    @tag("<c-a>/<c-[>/<escape>(hint[annotation])")
    def octivate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        super().octivate()
        self.app.stateman.setSubmode()
        self.app.delegman.delegate(
                mode='hint', 
                submode='annotation', 
                view=view, 
                action='octivate', 
                data=kwargs) 
