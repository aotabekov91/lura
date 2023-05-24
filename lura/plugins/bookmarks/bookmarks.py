#!/usr/bin/python3

from lura.utils import Plugin

from .create import Bookmark

class Bookmarks(Plugin):

    def __init__(self, app):
        super().__init__(app)
        self.bookmark=Bookmark(app)
