from plug import Plug, tag, deleg

class FitzSearch(Plug):

    def setup(self):
        super().setup()
        self.m_cache={}

    def find(self, view=None, search=None, **kwargs):
        found=[]
        if view and search:
            model=view.model()
            elements=model.elements()
            for pageno, elem in elements.items():
                page=elem.data()
                item=view.item(pageno)
                results=page.search_for(search)
                if results:
                    for result in results:
                        x, y = result.x0, result.y0
                        w, h = abs(result.x1-x), abs(result.y1-y)
                        unified=elem.unify((x, y, w, h))
                        found+=[{
                            'xrange': [pageno],
                            'box': [unified],
                            'item': item,
                            'result': result}]
        return found

    @deleg('search@(search)[FitzView]')
    def search(self, view=None, search=None, **kwargs):
        model=view.model()
        found=self.m_cache.get((model, search), None)
        if found is None:
            found=self.find(view=view, search=search, **kwargs)
            self.m_cache[(model, search)]=found
        return found

    @deleg('goTo@(search)[FitzView]')
    def goTo(self, kind='next', xrange=[1], view=None, data={}, **kwargs):
        if data:
            results=data.get('results')
            idx=self.app.delegman.delegate(
                    mode='search',
                    action='currentIndex',
                    data={'view': view})
            if idx is None:
                idx=0
            elif kind=='first':
                idx=1
            elif kind=='last':
                idx=len(results)
            elif kind=='next':
                idx+=xrange[-1]
            elif kind=='prev':
                idx-=xrange[-1]
            elif xrange:
                idx=xrange[-1]
            else:
                idx=None
            # TODO: some minor inconsistancies with jumping numbers
            print(idx, kind)
            if idx is not None:
                if idx+1>=len(results):
                    idx=1
                elif idx-1<=0:
                    idx=len(results)
                self.app.delegman.delegate(
                        mode='search',
                        action='setCurrentIndex',
                        data={'view': view, 'idx': idx})
                found=results[idx-1]
                xrange=found['xrange']
                box=found['box'][-1]
                x, y=box.x(), box.y()
                self.app.delegman.delegate(
                        mode='normal',
                        action='goTo',
                        view=view,
                        data={'view': view, 'x': x, 'y': y-0.1,  'xrange': xrange})
                selection=self.app.delegman.delegate(
                        action='createSelection', 
                        data={'view': view, 'data':found})
                self.app.delegman.delegate(
                        action='setSelection', 
                        data={'view': view, 'selection': selection})


            

