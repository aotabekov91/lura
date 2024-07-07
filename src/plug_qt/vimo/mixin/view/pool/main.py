from PyQt6 import QtCore

from ..items import Items
from .utils import Runner


class PoolItems(Items):
    canPool = True

    def setup(self):
        super().setup()
        self.pool = QtCore.QThreadPool()

    def setItems(self, m):
        self.m_items = {}
        sf = self.scaleFactor
        c = self.m_config.get("Item", {})
        c = Runner(
            model=m,
            config=c,
            view=self,
            scaleFactor=sf,
            klass=self.item_class,
        )
        c.signals.created.connect(self.setupItem)
        c.signals.finished.connect(self.setupModel)
        self.pool.start(c)

    def setupModel(self):
        self.redraw()
        self.modelLoaded.emit(self, self.m_model)
        self.modelChanged.emit(self.m_model)
