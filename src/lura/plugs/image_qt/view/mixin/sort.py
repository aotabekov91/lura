from gizmo.utils import tag

class Sort:

    canSort=True

    def sort(self, by='name'):

        if by=='name':
            self.sortByName()

    @tag('sN', modes=['command|^own'])
    def sortByNameReversed(self):
        self.sortByName(True)

    @tag('sn', modes=['command|^own'])
    def sortByName(self, reverse=False):

        def sort(item):
            e=item.element()
            return e.path()

        items=self.m_items.values()
        items=sorted(
                items, 
                key=sort, 
                reverse=reverse)
        sitems={}
        selems={}
        for i, item in enumerate(items):
            item.setIndex(i+1)
            elem=item.element()
            elem.setIndex(i+1)
            sitems[i+1]=item
            selems[i+1]=elem
        self.m_items=sitems
        self.m_model.setElements(selems)
        self.redraw()
