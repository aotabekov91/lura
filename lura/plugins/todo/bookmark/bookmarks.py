#!/usr/bin/python3

from tables import Bookmarks as Table
from lura.utils import Plugin

from .create import Bookmark as Creator
from .display import Bookmarks as Displayer

class Bookmarks(Plugin):

    def __init__(self, app):
        super().__init__(app)
        self.bookmark=Creator(app)
        self.bookmarks=Displayer(app)
        self.app.tables.add_table(Table, 'bookmarks')
