from plug import Plug, tag
from plug_qt.vimo.gizmo.view.list import ListWidgetView

class Bookmarks(Plug):

    locator='position'
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
        self.m_bookmarker=self.app.plugman.getPlug(
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
        model=view.model()
        bookmark_model=self.m_bookmarker.getModel(model)
        if bookmark_model and self.view!=view:
            self.view.setModel(bookmark_model)

    @tag('<c-b>(normal)')
    def toggle(self):
        self.view.toggle()

    @tag('O(normal)[BookmarkView]')
    def openAndFocus(self):
        self.open()
        view=self.app.stateman.subview()
        view.activate()

    @tag('o(normal)[BookmarkView]')
    def open(self):
        item=self.view.currentItem()
        if item: 
            data=item.element().data()
            view=self.app.stateman.subview()
            view.openLocator(data, kind=self.locator)

    @tag('d(normal)[BookmarkView]')
    def delete(self):
        item=self.view.currentItem()
        element=item.element()
        model=element.model()
        model.delBookmark(element)
