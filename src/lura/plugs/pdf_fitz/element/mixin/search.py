class Search:

    def setup(self):

        super().setup()
        self.m_search_cache={}

    def search(self, txt):

        c=self.m_search_cache.get(txt, None)
        if c: return c
        return self.m_data.search_for(txt)

    def extract(self, rect=None, box=None, kind=None):

        if box:
            rect=self.m_norm.mapRect(box)
        if rect:
            if kind=='text':
                x, y = rect.x(), rect.y()
                w, h = rect.width(), rect.height()
                r=(x, y, x+w, y+h)
                f=self.m_data.get_text(
                        'blocks', clip=r)
                if f: 
                    return f[0][4]
                return ''
