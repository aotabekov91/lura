class Links:

    hasLinks=True

    def setup(self):

        super().setup()
        self.m_links={}
        self.m_named_links={}
        self.m_links_cached=False

    def getLinks(self):

        if not self.m_links_cached:
            self.setLinks()
        return self.m_links

    def getLinkByName(self, name):

        if not self.m_links_cached:
            self.setLinks()
        return self.m_named_links.get(name, None)

    def setLinks(self):

        self.m_links=self.element().getLinks()
        for l in self.m_links:
            l['item']=self

    def setLinkProp(self, data):
        self.element().setLinkProp(data)
