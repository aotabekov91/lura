from plug import Plug, tag

class ElementListEdit(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addAgent()
        else:
            self.app.appSoonStarts.connect(
                    self.addAgent)

    def addAgent(self):
        holder=self.app.plugman.getPlug('Edit')
        if holder:
            holder.addAgent('update', 'ElementListView', self)
            holder.addAgent('populate', 'ElementListView', self)

    def activate(self, view=None, action=None, **kwargs):
        if view and action:
            functor=getattr(self, action, None)
            if functor:
                functor(view=view, **kwargs)

    @tag('<c-[>(normal)[ElementView]')
    def octivate(self, view=None, **kwargs):
        if not view:
            view=self.app.stateman.view()
        if view:
            manager=view.manager()
            if manager:
                manager.activate()

    def populate(self, view=None, **kwargs):
        item=view.currentItem()
        element_view=view.itemWidget(item)
        element_view.activate(mode='normal')
        idx=element_view.currentIndex()
        if idx[0] is None:
            element_view.goTo(kind='first')
        else:
            widget=element_view.widget(idx=idx)
            widget.setFocus()
        self.app.stateman.activate()
