from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtWidgets import QAbstractItemView as V

class Visual:

    hasVisual=True

    def setup(self):

        super().setup()
        self.m_visual_direction=None

        # self.moder.modeChanged.connect(
        #         self.setVisualMode)

    def setVisualMode(self, mode):

        if mode.name=='visual':
            self.m_visual_direction=None
            self.setSelectionMode(V.MultiSelection)
        else:
            self.setSelectionMode(V.SingleSelection)

    def visualGoTo(self, kind, rstart=1):

        for i in range(rstart):
            i=self.currentIndex()
            m=self.selectionModel()
            c1=self.m_visual_direction
            c2=kind!=self.m_visual_direction
            if c1 and c2: 
                mode=QItemSelectionModel.Toggle
                self.m_visual_direction=kind
                m.select(i, mode)
                return
            self.go(kind=kind)
        self.m_visual_direction=kind

    def visualGoToUp(self, rstart=1):
        self.visualGoTo('up', rstart)

    def visualGoToDown(self, rstart=1):
        self.visualGoTo('down', rstart)
