from plug import Plug, tag
from plug_qt.vimo.gizmo.view.list import ListWidgetView

class Bookmarks(Plug):

    default_mode='normal'
    position = {"BookmarkView": "D|L"}
    widget_map={
            'id': {'w':  'Label', 'p': '0x0x1x1'},
            'text': {'w': 'TextEdit', 'p': '1x0x1x1'}}

    def setup(self):
        super().setup()
        if self.app.running:
            self.setupView()
        else:
            self.app.appSoonStarts.connect(
                    self.setupView)

    def setupView(self):
        self.m_bookmarker=self.app.plugman.plugs.get(
                'Bookmark')
        if self.m_bookmarker:
            self.view=self.app.buffman.createView(
                    ListWidgetView, 
                    name='BookmarkView',
                    position=self.position,
                    widget_map=self.widget_map,
                    )
            self.app.stateman.viewChanged.connect(
                    self.updateView)

    def updateView(self, view):
        model=self.m_bookmarker.getModel(view)
        if model:
            self.view.setModel(model)

    @tag('<c-b>(normal)')
    def toggleOutline(self):
        self.view.toggle()

    @tag('o(normal)[^]')
    def openAndFocus(self):
        self.open(*args, **kwargs)
        t=self.app.buffman.type()
        t.activate()

    @tag('O(normal)[^]')
    def open(self):
        i=self.currentItem()
        t=self.app.buffman.type()
        if i: 
            d=i.element().data()
            t.openLocator(d, kind=self.locator)

    @tag('d(normal)[^]')
    def delete(self):
        i=self.currentItem()
        m=self.model()
        if i and m:
            e=i.element()
            m.delElement(e)
