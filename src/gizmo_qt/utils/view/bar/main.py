from . import base, mixin


class StatusBarView(
    mixin.Tabline,
    mixin.Editline,
    mixin.Powerline,
    base.BaseStatusBarView,
):
    def setup(self):
        super().setup()
        self.editWanted.connect(self.toggleTabline)

    def toggleTabline(self, cond):
        if cond:
            idx = self.edit.m_idx
        else:
            idx = self.tabline.m_idx
        self.stack.setCurrentIndex(idx)
