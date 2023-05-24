from tables import Bookmark
from lura.utils import Plugin
from plugin.utils import register

from .create import BookmarkCreator
from .display import BookmarkDisplayer

class BookmarkPlug(Plugin):

    def __init__(self, app):

        super().__init__(app) 

        self.app.tables.add_table(Bookmark, 'bookmark')

        self.bookmark=BookmarkCreator(app)
        self.bookmarks=BookmarkDisplayer(app)
