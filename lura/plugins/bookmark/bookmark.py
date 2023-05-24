from lura.utils import Plugin
from plugin.utils import register
from tables import Bookmark as Table

from .create import BookmarkCreator
from .display import BookmarkDisplayer

class Bookmark(Plugin):

    def __init__(self, app):

        super().__init__(app)
        self.bookmark=BookmarkCreator(app)
        self.bookmarks=BookmarkDisplayer(app)
        self.app.tables.add_table(Table, 'bookmark')
