from lura.gizmo.utils import hashdict


class Locate:
    canLocate = True

    def createLocator(self, data={}, **kwargs):
        return hashdict(data)

    def findLocator(self, prefix, kind, **kwargs):
        if kind:
            n = f"{prefix}{kind.title()}Locator"
            return getattr(self, n, None)

    def delLocator(self, data={}, kind=None, **kwargs):
        f = self.findLocator("del", kind)
        if f:
            return f(data, **kwargs)
        return self.m_model.delLocator(
            data=data, kind=kind, **kwargs
        )

    def getLocator(self, data={}, kind=None, **kwargs):
        f = self.findLocator("get", kind)
        if f:
            return f(data, **kwargs)
        return self.m_model.getLocator(
            data=data, kind=kind, **kwargs
        )

    def setLocator(self, data={}, kind=None, **kwargs):
        f = self.findLocator("set", kind)
        if f:
            return f(data, **kwargs)
        return self.m_model.setLocator(
            data=data, kind=kind, **kwargs
        )

    def openLocator(self, data={}, kind=None, **kwargs):
        f = self.findLocator("open", kind)
        if f:
            return f(data, **kwargs)
        return self.m_model.openLocator(
            data=data, kind=kind, **kwargs
        )
