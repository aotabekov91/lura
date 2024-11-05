from PyQt6 import QtCore

from plug import tag, Plug

from .model import BookmarkModel

class Bookmark(Plug, QtCore.QObject):

    modelCreated=QtCore.pyqtSignal(object)

    def setup(self):
        super().setup()
        self.m_models={}
        self.m_agents={}

    def addAgent(self, name, bookmarker):
        self.m_agents[name]=bookmarker

    def getAgent(self, name):
        return self.m_agents.get(name, None)

    def getModel(self, model):
        bookmark_model=self.m_models.get(model)
        if model and not bookmark_model:
            bookmark_model=self.createModel(model)
            self.m_models[model]=bookmark_model
        return bookmark_model

    def createModel(self, model):
        bookmark_model=BookmarkModel(source=model, agent=self)
        self.modelCreated.emit(bookmark_model)
        return bookmark_model

    @tag(["b(normal)" ,"<escape>/<c-[>(bookmark[any])"])
    def toggleBookmark(self):
        view=self.app.stateman.view()
        model=view.model()
        name=model.__class__.__name__
        bookmarker=self.getAgent(name)
        if bookmarker:
            mode=self.app.stateman.toggle(
                mode="bookmark",
                passive=["bookmark"])
            if mode=='bookmark':
                self.activateEdit(view)
            else:
                self.app.view.bar.octivateEdit()
                self.app.stateman.toggle()

    @tag("<enter>/<return>(bookmark)")
    def bookmark(self):
        view=self.app.stateman.view()
        model=view.model()
        bookmark_model=self.getModel(model)
        bookmark = self.app.view.bar.text()
        bookmark_model.addBookmark(
                model, view, {"text": bookmark})
        self.toggleBookmark()

    def activateEdit(self, view):
        model=view.model()
        bookmark_model=self.getModel(model)
        loc = view.getLocator(kind="position")
        position = loc.get("position")
        bookmark=bookmark_model.getBookmark(
                position, by="position")
        text=''
        if bookmark:
            text=bookmark.data("text")
        self.app.view.bar.activateEdit(edit=text)
