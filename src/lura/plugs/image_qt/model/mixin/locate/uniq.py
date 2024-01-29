class UniqLocate:

    def getUniqLocator(
            self, 
            data={}, 
            agent=None,
            **kwargs,
            ):

        data['kind']=self.kind
        if agent=='model':
            idx=[]
            for i, e in self.m_elements.items(): 
                d=self.createLocator(data)
                d['hash']=e.identifier()
                idx+=[d]
            return idx
        else:
            i=kwargs.get('item')
            if i: 
                e=i.element()
                data['hash']=e.identifier()
            else:
                data['hash']=self.id()
        return self.createLocator(data)
