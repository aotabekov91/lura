from plug import Plug

class Copy(Plug):

    def setup(self):
        super().setup()
        self.m_copiers={}

    def addCopier(self, name, copier):
        self.m_copiers[name]=copier

    def copier(self, name):
        return self.m_copiers.get(name, None)

    def copy(self, obj):
        name=obj.__class__.__name__
        copier=self.copier(name)
        if copier:
            return copier.copy(obj)
