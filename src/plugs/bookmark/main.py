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
        if view:
            model=view.model()
            functor=self.app.delegman.getAgent(
                    'normal', None, view, 'goTo')
            if functor and model:
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
        editor=self.app.plugman.getPlug('Editline')
        position=self.app.delegman.delegate(
                mode='normal', view=view, action='goToState')
        bookmark=bookmark_model.getBookmark(
                position, by="position")
        text=''
        if bookmark:
            text=bookmark.data("text")
        editor.activate(edit=text, mode='bookmark')

    def octivate(self):
        editor=self.app.plugman.getPlug('Editline')
        if editor:
            editor.octivate()
        self.app.stateman.activate()

    @tag("<enter>/<return>(bookmark)")
    def bookmark(self, view=None, text=None):
        if not view:
            view=self.app.stateman.subview()
        if view:
            model=view.model()
            bmodel=self.getModel(model)
            if not text:
                editline=self.app.plugman.getPlug('Editline')
                text=editline.text()
            position=self.app.delegman.delegate(
                    'normal', action='goToState', view=view)
            if position and bmodel:
                data={
                        'text': text,
                        'position': position,
                        'source_id': model.id(),
                     }
                bmodel.addBookmark(data)
            self.octivate()
