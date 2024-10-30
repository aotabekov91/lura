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
        bookmarker=self.app.plugman.plugs.get(
                'Bookmark')
        if bookmarker:
            bookmarker.addAgent(
                    'FitzView', self)

    def getBookmark(self, model, view, position=None):
        if not position:
            loc = view.getLocator(kind="position")
            position = loc.get("position")
        return model.getBookmark(position, by="position")

    def setBookmark(self, model, view, text=None):
        if not text:
            text = self.app.view.bar.text()
        data = {"text": text}
        data = view.getLocator(data=data, kind="uniq")
        data = view.getLocator(data=data, kind="position")
        return model.addBookmark(data)

    def delBookmark(self, model, view, data):
        return model.delBookmark(data=data)
