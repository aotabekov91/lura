class Cache:
    canCache = True

    def setup(self):
        self.m_cache = {}
        super().setup()

    def setCache(self, key, value, name="default"):
        self.m_cache[name][key] = value

    def clearCache(self, name="default"):
        self.m_cache[name] = {}

    def addCache(self, name="default", holder={}):
        if not name in self.m_cache:
            self.m_cache[name] = holder

    def dropCache(self, key, name="default"):
        if name in self.m_cache:
            d = self.m_cache[name].pop(key, None)

    def getCache(self, key=None, name="default"):
        cache = self.m_cache.get(name, {})
        if key:
            return cache.get(key, None)
        return cache
