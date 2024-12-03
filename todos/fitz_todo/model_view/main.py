from gizmo.utils import tag
from gizmo.plug import Plug

from .tab import Tab
from .tree import TreeView
from .lwidget import ListWidgetView

class ModelView(Plug):

    def setup(self):

        super().setup()
        self.createTabs()
        self.app.buffman.addViewer(
                TreeView)
        self.app.buffman.addViewer(
                ListWidgetView)

    def createTabs(self):

        for n, d in self.m_config.items():
            name=f'{n}Tab'
            position=d.get('position', {})
            prefix_keys=d.get('tab_prefix', {})
            tab=Tab(
                    config=d,
                    name=name,
                    app=self.app, 
                    identifier=name,
                    position=position,
                    prefix_keys=prefix_keys,
                    )
            self.app.buffman.saveView(name, tab)
            self.app.buffman.locate(tab)
