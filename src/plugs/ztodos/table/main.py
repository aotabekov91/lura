from gizmo.plug import Plug

from . import tables
from .model import Model

class Table(Plug):

    name='dbtables'

    def setup(self):

        super().setup()
        self.m_models={}
        self.updateSettings()
        self.app.tools[self.name]=self
        self.app.buffman.modelLoaded.connect(
                self.attachModel)

    def updateSettings(self):

        g=self.m_config.pop('General', {})
        for n, d in self.m_config.items():
            c=g.copy()
            c.update(d)
            tn=c.get('table', n)
            name=d.get('name', n)
            tc=getattr(tables, tn, None)
            if tc:
                table=tc()
                m=Model(
                        config=c,
                        name=name, 
                        table=table,
                        app=self.app,
                        )
                self.m_models[name]=m

    def attachModel(self, m):

        for n, t in self.m_models.items():
            t.handleModel(m)
