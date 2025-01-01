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
        if view and normal:
            model=view.model()
            agent=normal.getAgent(action='goTo', view=view)
            if model and agent:
                bookmark_model=BookmarkModel(source=model)
                self.m_models[model]=bookmark_model
                self.modelCreated.emit(bookmark_model)

    @tag(["b(normal)" ,"<escape>/<c-[>(bookmark[any])"])
    def toggle(self):
        view=self.app.stateman.subview()
        editor=self.app.plugman.getPlug('Editline')
        if view and editor:
            model=self.getModel(view.model())
            if model:
                mode=self.app.stateman.activate(
                    mode="bookmark",
                    passive=["bookmark"],
                    toggle_mode=True)
                if mode=='bookmark':
                    self.activate()
                else:
                    self.octivate()

    def activate(self):
        view=self.app.stateman.view()
        model=view.model()
        bookmark_model=self.getModel(model)
        normal=self.app.plugman.getPlug('Normal')
        editor=self.app.plugman.getPlug('Editline')
        text=''
        if normal:
            position=normal.getState(state='goTo', view=view)
            bookmark=bookmark_model.getBookmark(
                    position, by="position")
            if bookmark:
                text=bookmark.data("text")
        editor.activate(edit=text, mode='bookmark')

    def octivate(self):
        editor=self.app.plugman.getPlug('Editline')
        if editor:
            editor.octivate()
        self.app.stateman.activate()

    @tag("<enter>/<return>(bookmark)")
    def bookmark(self):
        view=self.app.stateman.subview()
        model=view.model()
        bookmark_model=self.getModel(model)
        editline=self.app.plugman.getPlug('Editline')
        bookmark=editline.text()
        normal=self.app.plugman.getPlug('Normal')
        position=normal.getState(view=view, state='goTo')
        if normal and bookmark_model:
            data={
                    'text': bookmark,
                    'position': position,
                    'source_id': model.id(),
                 }
            bookmark_model.addBookmark(data)
        self.octivate()
