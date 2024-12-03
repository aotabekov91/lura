import gizmo

class OutlineView(
        gizmo.ui.qt.mixin.view.Fullscreen,
        gizmo.ui.qt.utils.view.TreeView,
        ):

    canFollow=True
    default_mode='normal'
    position={'OutlineView': 'D|L'}
    section_ratios={0: .75, 1: .25}

    def updateKlass(self):

        super().updateKlass()
        self.section_ratios=self.m_kwargs.get(
                'section_ratios', self.section_ratios)

    def updateHeaderRatio(self):

        header=self.header()
        ratio=self.section_ratios
        width=self.size().width()
        for i, v in ratio.items():
            header.resizeSection(
                    i, int(width*v))

    def setup(self):
        
        super().setup()
        self.resized.connect(self.updateHeaderRatio)
