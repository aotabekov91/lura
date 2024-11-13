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
        model=view.model()
        annotation_model=self.m_annotate.getModel(model)
        if annotation_model and self.view!=view:
            self.view.setModel(annotation_model)

    @tag('<c-A>(normal)')
    def toggleAnnotations(self):
        self.view.toggle()

    @tag('O(normal)[AnnotationView]')
    def openAndFocus(self):
        self.open()
        t=self.app.buffman.type()
        t.activate()

    @tag('o(normal)[AnnotationView]')
    def open(self):
        item=self.view.currentItem()
        if item: 
            data=item.element().data()
            view=self.app.stateman.subview()
            x, y = 0, 0
            page=data.get('page', 0)
            boxes=data.get('box')
            if boxes:
                box=boxes[0]
                x=box.x()
                y=box.y()
            view.goTo(page, x, y)

    @tag('d(normal)[AnnotationView]')
    def delete(self):
        item=self.view.currentItem()
        if item:
            element=item.element()
            view=self.app.stateman.subview()
            model=view.model()
            annotator=self.app.plugman.plugs.get('Annotate')
            selector=self.app.plugman.plugs.get('Selection')
            annotation_model=annotator.getModel(model)
            annotation_model.delAnnotate(element)
            if selector:
                selector.cleanUpSelection(view)
