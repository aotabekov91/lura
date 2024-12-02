from . import base, mixin


class StatusBarView(
    mixin.Editline,
    base.BaseStatusBarView,
):
    def setup(self):
        super().setup()
        self.editWanted.connect(self.toggleTabline)
        self.show()

    def toggleTabline(self, cond):
        if cond:
            idx = self.edit.m_idx
        else:
            idx = self.tabline.m_idx
        self.stack.setCurrentIndex(idx)
