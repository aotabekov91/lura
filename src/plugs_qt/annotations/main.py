from plug import Plug, tag
from plug_qt.vimo.gizmo.view.list import ListWidgetView

class Annotations(Plug):

    default_mode='normal'
    position = {"AnnotationView": "D|L"}
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
        self.m_annotate=self.app.plugman.plugs.get(
                'Annotate')
        if self.m_annotate:
            self.view=self.app.buffman.createView(
                    ListWidgetView, 
                    name='AnnotationView',
                    position=self.position,
                    widget_map=self.widget_map,
                    )
            self.app.stateman.viewChanged.connect(
                    self.updateView)

    def updateView(self, view):
        model=self.m_annotate.getModel(view)
        print(view, model)
        if model and self.view!=view:
            self.view.setModel(model)

    @tag('<c-A>(normal)')
    def toggleAnnotations(self):
        self.view.toggle()

    @tag('o(normal)[AnnotationView]')
    def openAndFocus(self):
        self.open()
        t=self.app.buffman.type()
        t.activate()

    @tag('O(normal)[^]')
    def open(self):
        item=self.view.currentItem()
        tipe=self.app.buffman.type()
        if item: 
            data=item.element().data()
            tipe.openLocator(data, kind=self.locator)

    @tag('d(normal)[^]')
    def delete(self):
        i=self.currentItem()
        m=self.model()
        if i and m:
            e=i.element()
            m.delElement(e)
