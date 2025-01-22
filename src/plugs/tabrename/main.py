from plug import Plug, tag

class Tabrename(Plug):

    @tag("<c-t>r(normal)")
    def activateTabRename(self, xrange=None):
        raise
        bar=self.app.view.bar
        if bar.current:
            idx = bar.current.currentIndex()
            if xrange:
                idx = xrange[-1] - 1
            self.activate()
            self.app.stateman.setSubmode("rename")
            w = bar.current.widget(idx)
            self.rename_widget = w
            self.active(edit=w.m_tab_name)

    @tag("<enter>/<return>(edit[tab])")
    def rename(self):
        w = self.rename_widget
        if self.current and w:
            n = self.app.view.bar.edit.text()
            w.m_tab_name = n
            self.updateTabLabels(tab=self.current)
        self.octivateEdit()
