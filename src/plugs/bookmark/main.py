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

    def getModel(self, view):
        model=view.model()
        bookmark_model=self.m_models.get(model)
        if model and not bookmark_model:
            bookmark_model=self.createModel(model)
            self.m_models[model]=bookmark_model
        return bookmark_model

    @tag(["b(normal)" ,"<escape>/<c-[>(bookmark[any])"])
    def toggleBookmark(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
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
    def setBookmark(self):
        view=self.app.stateman.view()
        name=view.__class__.__name__
        bookmark_model=self.getModel(view)
        bookmarker=self.getAgent(name)
        bookmarker.setBookmark(bookmark_model, view)
        self.toggleBookmark()

    def createModel(self, model):
        model=BookmarkModel(source=model)
        self.modelCreated.emit(model)
        return model

    def activateEdit(self, view):
        name=view.__class__.__name__
        bookmarker=self.getAgent(name)
        bookmark_model=self.getModel(view)
        bookmark=bookmarker.getBookmark(
                bookmark_model, view)
        text=''
        if bookmark:
            text=bookmark.data("text")
        self.app.view.bar.activateEdit(edit=text)
