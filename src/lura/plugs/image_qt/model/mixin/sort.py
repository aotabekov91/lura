class Sort:

    canSort=True

    def sort(self, by='name'):
        if by=='name':
            return self.sortByName()

    def sortByName(self):

        f=lambda e: e.path()
        elems=self.m_elements.values()
        elems=sorted(elems, f)
        sorted_elems={}
        for i, e in enumerate(elems):
            sorted_elems[i]=e
        return sorted_elems
