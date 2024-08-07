from plug.utils import tag


class AppGo:
    @tag("ga(normal)")
    def goToApp(self, xrange=None, **kwargs):
        if not type(xrange) == int:
            return
        if not self.checkProp("hasServer", self.app):
            return
        req = {
            "target": xrange,
            "object": "app.view",
            "action": "activateWindow",
        }
        return self.app.server.request(**req)
