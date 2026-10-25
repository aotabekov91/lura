from plug import Plug, tag
from plug_qt.gizmo import ElementListView

class Bookmarks(Plug):

    locator='position'
    default_mode='normal'
    position = {"BookmarkView": "D|R"}
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
                    ElementListView, 
                    name='BookmarkView',
                    attributes=[
                        {
                        'key': 'position', 
                        'value': self.position, 
                        },
                        {
                        'key': 'widget_map', 
                        'value': self.widget_map, 
                        'copy':True,
                        }])
            self.app.stateman.viewChanged.connect(
                    self.updateView)

    def updateView(self, view):
        model=view.model()
        bookmark_model=self.m_bookmarker.getModel(model)
        if bookmark_model and self.view!=view:
            self.view.setModel(bookmark_model)

    @tag('<c-B>(normal)')
    def toggle(self):
        self.view.toggle()

    @tag('O(normal)[BookmarkView]')
    def openAndFocus(self):
        self.open()
        view=self.app.stateman.subview()
        if view:
            view.activate()

    @tag('o(normal)[BookmarkView]')
    def open(self, view=None):
        if not view:
            view=self.app.stateman.subview()
        item=self.view.currentItem()
        if item: 
            data=item.element().data()
            position=data.get('position')
            # todo: different views same model bookmark opens only in the first view
            # pos_view=position.get('view', None)
            # print(data)
            # if pos_view!=view and view:
            #     source_id=data.get('source_id', None)
            #     model_id=view.model().id()
                # if source_id==model_id:
                #     position['view']=view
            self.app.delegman.delegate(
                    mode='normal', 
                    view=view, 
                    action='goTo', 
                    data=position)

    @tag('d(normal)[BookmarkView]')
    def delete(self):
        item=self.view.currentItem()
        element=item.element()
        bmodel=element.model()
        bmodel.remove(element)
