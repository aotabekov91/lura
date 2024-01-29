from gizmo.utils import tag
from gizmo.vimo.view import TabView

class FilesTab(TabView):

    canRelabel=False
    initial_create=False
    prefix_keys={'command': 'f'}
    position={'FilesTab': 'D|L'}

    def addView(self, v, **kwargs):

        v=super().addView(v, **kwargs)
        if not self.current:
            kwargs['focus']=False
            self.setView(v, **kwargs)

    @tag('t', modes=['command'])
    def toggle(self):
        super().toggle()
