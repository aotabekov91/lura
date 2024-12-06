from plug.utils import tag


class AppClose:

    @tag("<c-Q>(normal)")
    def close(self, xrange):
        if self.checkProp("hasServer", self.app):
            self.app.server.request(
                object="app",
                target=xrange,
                action="quit",
            )
