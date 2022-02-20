from .cursor import Cursor


class View:

    def __init__(self, parent, settings):
        self.name='view'
        self.s_settings=settings
        self.cursor=Cursor(parent, settings.get('Cursor', {}))
