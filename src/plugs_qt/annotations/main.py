from plug import Plug, tag
from plug_qt.gizmo import ElementListView

class Annotations(Plug):

    default_mode='normal'
    position = {"AnnotationsView": "D|L"}
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
        self.m_annotate=self.app.plugman.getPlug(
                'Annotate')
        if self.m_annotate:
            self.view=self.app.buffman.createView(
                    ElementListView, 
                    name='AnnotationsView',
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

    @tag('O(normal)[AnnotationsView]')
    def openAndFocus(self):
        self.open(focus=True)

    @tag('o(normal)[AnnotationsView]')
    def open(self, focus=False, select=True, **kwargs):
        item=self.view.currentItem()
        normal=self.app.plugman.getPlug('Normal')
        selection=self.app.plugman.getPlug('Selection')
        if item and normal: 
            element=item.element()
            data=element.data()
            view=self.app.stateman.subview()
            x, y = 0, 0
            page=data.get('page', 0)
            boxes=data.get('box')
            if boxes:
                box=boxes[0]
                x=box.x()
                y=box.y()
            data['item']=view.item(page)
            normal.activate(action='goTo', view=view, xrange=[page], x=x, y=y, center=True)
            if select and selection:
                selection.select(view, selection=element)
            if focus:
                view.activate()

    @tag('d(normal)[AnnotationsView]')
    def delete(self):
        item=self.view.currentItem()
        if item:
            element=item.element()
            view=self.app.stateman.subview()
            model=view.model()
            annotator=self.app.plugman.getPlug('Annotate')
            selector=self.app.plugman.getPlug('Selection')
            annotation_model=annotator.getModel(model)
            annotation_model.delAnnotate(element)
            if selector:
                selector.cleanUpSelection(view)
