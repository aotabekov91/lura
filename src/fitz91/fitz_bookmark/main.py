from plug import Plug

class FitzBookmark(Plug):

    def setup(self):
        super().setup()
        if self.app.running:
            self.addToBookmarker()
        else:
            self.app.appSoonStarts.connect(
                    self.addToBookmarker)

    def addToBookmarker(self):
        bookmarker=self.app.plugman.getPlug(
                'Bookmark')
        if bookmarker:
            bookmarker.addAgent(
                    'FitzModel', self)

    def getBookmark(self, model, view, position=None):
        if not position:
            loc = view.getLocator(kind="position")
            position = loc.get("position")
        return model.getBookmark(position, by="position")

    def activate(self, view, data):
        data = view.getLocator(data=data, kind="uniq")
        data = view.getLocator(data=data, kind="position")
        return data

    def delBookmark(self, model, view, data):
        return model.delBookmark(data=data)
