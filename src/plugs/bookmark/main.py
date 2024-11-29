from PyQt6 import QtCore

from plug import tag, Plug

from .model import BookmarkModel

class Bookmark(Plug, QtCore.QObject):

    modelCreated=QtCore.pyqtSignal(object)

    def setup(self):
        super().setup()
        self.m_models={}
        self.app.buffman.viewCreated.connect(
                self.createModel)

    def getModel(self, model):
        return self.m_models.get(model, None)

    def createModel(self, view):
        normal=self.app.plugman.getPlug('Normal')
        if normal:
            position=normal.currentPosition(view=view)
            if position:
                model=view.model()
                bookmark_model=BookmarkModel(source=model)
                self.m_models[model]=bookmark_model
                self.modelCreated.emit(bookmark_model)

    @tag(["b(normal)" ,"<escape>/<c-[>(bookmark[any])"])
    def toggleBookmark(self):
        view=self.app.stateman.view()
        if view:
            model=view.model()
            bookmark_model=self.getModel(model)
            if bookmark_model:
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
        normal=self.app.plugman.getPlug('Normal')
        if normal and bookmark_model:
            data={
                    'text': bookmark,
                    'source_id': model.id(),
                    'position': normal.currentPosition(view=view),
                 }
            bookmark_model.addBookmark(data)
            self.toggleBookmark()

    def activateEdit(self, view):
        model=view.model()
        bookmark_model=self.getModel(model)
        normal=self.app.plugman.getPlug('Normal')
        text=''
        if normal:
            position=normal.currentPosition(view=view)
            bookmark=bookmark_model.getBookmark(
                    position, by="position")
            if bookmark:
                text=bookmark.data("text")
        self.app.view.bar.activateEdit(edit=text)
